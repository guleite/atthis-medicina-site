/* ATTHIS — interações do site (JS puro, sem dependências) */
(() => {
  const d = document, w = window;
  const reduce = w.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));

  /* ================= Tela de loading + transição entre páginas ================= */
  const html = d.documentElement;
  const loader = d.querySelector('.loader');
  if (loader) {
    const bar = loader.querySelector('.loader__bar i');
    const isReturn = html.classList.contains('is-return');
    const minTime = reduce ? 150 : (isReturn ? 380 : 1650);
    const t0 = performance.now();
    const imgs = [...d.images].filter(i => i.loading !== 'lazy' && !loader.contains(i));
    const total = imgs.length + 1;
    let loaded = 0, finished = false;
    const tick = () => { if (bar) bar.style.transform = `scaleX(${Math.min(1, (loaded + .4) / (total + .4))})`; };
    const one = () => { loaded++; tick(); };
    imgs.forEach(i => { if (i.complete) loaded++; else { i.addEventListener('load', one, { once: true }); i.addEventListener('error', one, { once: true }); } });
    if (d.fonts && d.fonts.ready) d.fonts.ready.then(one); else loaded++;
    tick();
    const finish = () => {
      if (finished) return; finished = true;
      if (bar) bar.style.transform = 'scaleX(1)';
      const wait = Math.max(0, minTime - (performance.now() - t0)) + (isReturn ? 60 : 280);
      setTimeout(() => {
        loader.classList.add('is-done');
        html.classList.remove('js-loading');
        try { sessionStorage.setItem('atthis-v', '1'); } catch (e) { /* modo privado */ }
        setTimeout(() => loader.classList.add('is-hidden'), 1400);
      }, wait);
    };
    if (d.readyState === 'complete') finish(); else w.addEventListener('load', finish);
    setTimeout(finish, isReturn ? 2500 : 4200); /* nunca segura o visitante por muito tempo */

    /* cortina ao clicar em links internos */
    d.addEventListener('click', e => {
      const a = e.target.closest('a[href]');
      if (!a || e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      if ((a.target && a.target !== '_self') || a.hasAttribute('download') || reduce) return;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || !/^https?:$/.test(url.protocol)) return;
      if (url.pathname === location.pathname && url.search === location.search) return; /* âncora na mesma página */
      e.preventDefault();
      d.body.classList.remove('menu-open');
      loader.classList.remove('is-done', 'is-hidden', 'is-covered');
      void loader.offsetWidth;
      loader.classList.add('is-leaving');
      setTimeout(() => loader.classList.add('is-covered'), 10);
      try { sessionStorage.setItem('atthis-v', '1'); } catch (err) { /* modo privado */ }
      setTimeout(() => { location.href = url.href; }, 820);
    });
    /* voltar pelo histórico (página guardada em cache) */
    w.addEventListener('pageshow', e => {
      if (!e.persisted) return;
      loader.classList.remove('is-leaving', 'is-covered');
      loader.classList.add('is-done', 'is-hidden');
      html.classList.remove('js-loading');
    });
  }

  /* Cabeçalho e botão flutuante */
  const header = d.querySelector('.site-header');
  const wa = d.querySelector('.wa-float');

  /* Menu mobile */
  const toggle = d.querySelector('.nav-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const open = d.body.classList.toggle('menu-open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    d.querySelectorAll('.mobile-menu a').forEach(a => a.addEventListener('click', () => d.body.classList.remove('menu-open')));
    d.addEventListener('keydown', e => { if (e.key === 'Escape') d.body.classList.remove('menu-open'); });
  }

  /* Revelar ao rolar */
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  d.querySelectorAll('[data-stagger]').forEach(p => [...p.children].forEach((c, i) => {
    c.style.setProperty('--i', i);
    if (!c.hasAttribute('data-reveal')) c.setAttribute('data-reveal', '');
  }));
  d.querySelectorAll('[data-reveal]').forEach(el => io.observe(el));

  /* Brilho que segue o cursor nos cartões */
  d.querySelectorAll('.area-card').forEach(c => {
    c.addEventListener('pointermove', e => {
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', `${e.clientX - r.left}px`);
      c.style.setProperty('--my', `${e.clientY - r.top}px`);
    });
  });

  /* Manifesto: palavras acendem conforme a rolagem */
  const mf = d.querySelector('[data-words]');
  let words = [];
  if (mf) {
    const html = mf.innerHTML.trim();
    const tmp = d.createElement('div'); tmp.innerHTML = html;
    const out = [];
    tmp.childNodes.forEach(n => {
      const isEm = n.nodeName === 'EM';
      (n.textContent || '').split(/\s+/).filter(Boolean).forEach(t => out.push(`<span class="w${isEm ? ' em' : ''}">${t}</span>`));
    });
    mf.innerHTML = out.join(' ');
    words = [...mf.querySelectorAll('.w')];
  }

  /* Jornada: cartões empilhados */
  const cards = [...d.querySelectorAll('.stack-card')];
  const steps = [...d.querySelectorAll('.journey__steps li')];
  const bar = d.querySelector('.journey__progress i');
  const stackWrap = d.querySelector('.stack');

  /* Parallax das imagens flutuantes */
  const floaters = [...d.querySelectorAll('[data-speed]')];

  /* Barra de leitura do artigo */
  const rp = d.querySelector('.read-progress');
  const article = d.querySelector('.article-body');
  const tocLinks = [...d.querySelectorAll('.toc a')];
  const heads = tocLinks.map(a => d.querySelector(a.getAttribute('href'))).filter(Boolean);

  let ticking = false;
  function frame() {
    ticking = false;
    const y = w.scrollY, vh = w.innerHeight;
    if (header) header.classList.toggle('is-scrolled', y > 24);
    if (wa) wa.classList.toggle('is-visible', y > vh * 0.5);

    if (words.length) {
      const r = mf.getBoundingClientRect();
      const p = clamp((vh * 0.82 - r.top) / (r.height + vh * 0.3));
      const lit = Math.round(p * words.length);
      words.forEach((s, i) => s.classList.toggle('is-lit', i < lit));
    }

    if (cards.length) {
      let active = 0;
      cards.forEach((c, i) => {
        const next = cards[i + 1];
        let p = 0;
        if (next) {
          const top = parseFloat(getComputedStyle(next).top) || 0;
          const nr = next.getBoundingClientRect();
          p = clamp(1 - (nr.top - top) / (vh * 0.75));
        }
        if (!reduce) c.style.setProperty('--p', p.toFixed(3));
        const ct = parseFloat(getComputedStyle(c).top) || 0;
        if (c.getBoundingClientRect().top <= ct + 60) active = i;
      });
      steps.forEach((s, i) => s.classList.toggle('is-active', i === active));
      if (bar && stackWrap) {
        const r = stackWrap.getBoundingClientRect();
        bar.style.width = `${clamp((vh * 0.35 - r.top) / (r.height - vh * 0.5)) * 100}%`;
      }
    }

    if (!reduce) floaters.forEach(f => {
      const r = f.parentElement.getBoundingClientRect();
      const off = (r.top + r.height / 2 - vh / 2) * parseFloat(f.dataset.speed);
      f.style.transform = `translate3d(0, ${off.toFixed(1)}px, 0)`;
    });

    if (rp && article) {
      const r = article.getBoundingClientRect();
      rp.style.width = `${clamp(-r.top / (r.height - vh)) * 100}%`;
    }
    if (heads.length) {
      let cur = 0;
      heads.forEach((h, i) => { if (h.getBoundingClientRect().top < vh * 0.3) cur = i; });
      tocLinks.forEach((a, i) => a.classList.toggle('is-active', i === cur));
    }
  }
  const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  w.addEventListener('scroll', onScroll, { passive: true });
  w.addEventListener('resize', onScroll);
  frame();

  /* Contadores */
  const cio = new IntersectionObserver(entries => entries.forEach(e => {
    if (!e.isIntersecting) return;
    cio.unobserve(e.target);
    const el = e.target, end = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
    if (reduce) { el.textContent = end.toLocaleString('pt-BR', { minimumFractionDigits: dec }); return; }
    const t0 = performance.now(), dur = 2000;
    const tick = t => {
      const k = clamp((t - t0) / dur), v = end * (1 - Math.pow(1 - k, 4));
      el.textContent = v.toLocaleString('pt-BR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
      if (k < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }), { threshold: 0.5 });
  d.querySelectorAll('[data-count]').forEach(el => cio.observe(el));

  /* FAQ: um aberto por vez dentro do grupo */
  d.querySelectorAll('.faq').forEach(g => {
    const items = [...g.querySelectorAll('details')];
    items.forEach(it => it.addEventListener('toggle', () => {
      if (it.open) items.forEach(o => { if (o !== it) o.open = false; });
    }));
  });

  /* Stepper (Como funciona) */
  const tabs = [...d.querySelectorAll('.stepper__tab')];
  const figs = [...d.querySelectorAll('.stepper__stage figure')];
  let stepIdx = 0, timer;
  const setStep = i => {
    stepIdx = i;
    tabs.forEach((t, k) => { t.classList.toggle('is-active', k === i); t.setAttribute('aria-selected', String(k === i)); });
    figs.forEach((f, k) => f.classList.toggle('is-active', k === i));
  };
  if (tabs.length) {
    tabs.forEach((t, i) => t.addEventListener('click', () => { setStep(i); clearInterval(timer); }));
    if (!reduce) timer = setInterval(() => setStep((stepIdx + 1) % tabs.length), 6000);
  }

  /* Filtro do blog */
  const filters = [...d.querySelectorAll('.filter')];
  const posts = [...d.querySelectorAll('.posts [data-cat]')];
  filters.forEach(f => f.addEventListener('click', () => {
    filters.forEach(x => x.classList.toggle('is-active', x === f));
    const c = f.dataset.filter;
    posts.forEach(p => {
      const show = c === 'todos' || p.dataset.cat === c;
      p.classList.toggle('post-card--hidden', !show);
      if (show) { p.classList.remove('is-in'); requestAnimationFrame(() => p.classList.add('is-in')); }
    });
  }));

  /* Botões lado a lado ou empilhados com a mesma largura */
  const equalize = () => {
    d.querySelectorAll('.btn-row, .cta__side').forEach(g => {
      const bs = [...g.children].filter(c => c.classList.contains('btn'));
      if (bs.length < 2) return;
      bs.forEach(b => { b.style.minWidth = ''; });
      const m = Math.max(...bs.map(b => b.getBoundingClientRect().width));
      if (m > 0) bs.forEach(b => { b.style.minWidth = `${Math.ceil(m)}px`; });
    });
  };
  equalize();
  if (d.fonts && d.fonts.ready) d.fonts.ready.then(equalize);
  let eqT; w.addEventListener('resize', () => { clearTimeout(eqT); eqT = setTimeout(equalize, 150); });

  /* ================= Pré-agendamento (pop-up e página de contato) ================= */
  const WA = '5561992831370';
  const ASIDE = [
    ['Vamos cuidar de você.', 'Em poucos passos, a Dra. Aclair entende o que você busca antes mesmo da primeira conversa.'],
    ['Cada história é única.', 'Conte o que motivou a sua busca. Pode escolher mais de uma área.'],
    ['Metas que fazem sentido.', 'Seus objetivos orientam o plano de cuidado, construído junto com você.'],
    ['Um retrato inicial.', 'Informações gerais ajudam a preparar a consulta. Os detalhes ficam para a conversa.'],
    ['Do seu jeito.', 'Presencial na Asa Sul ou por telemedicina: escolha o formato que cabe na sua rotina.'],
    ['Quase lá.', 'Revise as informações. Ao enviar, o WhatsApp abre com a mensagem pronta para a equipe.']
  ];

  function Booking(root) {
    const form = root.querySelector('form');
    const steps = [...root.querySelectorAll('.bstep')].filter(s => s.dataset.step !== 'done');
    const done = root.querySelector('.bstep[data-step="done"]');
    const next = root.querySelector('[data-next]');
    const nextLabel = root.querySelector('[data-next-label]');
    const nextIcon = root.querySelector('[data-next-icon]');
    const arrowIcon = nextIcon.innerHTML;
    const waIcon = '<svg class="wa-ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.5-5.26c0-5.45 4.43-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.89 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89a11.82 11.82 0 0 0-3.48-8.41Z"/></svg>';
    const prev = root.querySelector('[data-prev]');
    const bar = root.querySelector('[data-bar]');
    const num = root.querySelector('[data-step-num]');
    const aside = root.querySelector('.booking__aside');
    const aTitle = root.querySelector('[data-aside-title]');
    const aText = root.querySelector('[data-aside-text]');
    const lis = [...root.querySelectorAll('.booking__steps li')];
    const last = steps.length - 1;
    let i = 0, max = 0, url = '';

    const val = n => ((form.elements[n] && form.elements[n].value) || '').trim();
    const sel = n => [...form.querySelectorAll(`[name="${n}"]:checked`)].map(x => x.value);
    const one = n => sel(n)[0] || '';
    const first = () => { const f = val('nome').split(/\s+/)[0] || ''; return f ? f.charAt(0).toUpperCase() + f.slice(1) : ''; };
    const esc = s => s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

    function data() {
      const para = one('para');
      const objetivos = sel('objetivo'); if (val('outro')) objetivos.push(val('outro'));
      return [
        ['Nome', val('nome')],
        ['WhatsApp', val('telefone')],
        ['E-mail', val('email')],
        ['Consulta para', para ? (para === 'Mim' ? 'Para mim' : `Para ${para.toLowerCase()}`) + (val('familiar') && para !== 'Mim' ? ` (${val('familiar')})` : '') : ''],
        ['Áreas de interesse', sel('area').join(', ')],
        ['Objetivos', objetivos.join(', ')],
        ['Faixa etária', one('idade')],
        ['Acompanhamento médico atual', one('acomp')],
        ['Condições já diagnosticadas', sel('condicao').join(', ')],
        ['Formato', one('formato')],
        ['Melhor período', one('periodo')],
        ['Como conheceu', one('origem')],
        ['Mensagem', val('mensagem')]
      ].filter(r => r[1]);
    }
    function message() {
      const rows = data();
      const lines = ['Olá! Gostaria de agendar uma consulta com a Dra. Aclair Dallagranna.', '', '*Pré-agendamento pelo site Atthis*'];
      rows.forEach(([k, v]) => { if (k !== 'Mensagem') lines.push(`• ${k}: ${v}`); });
      const m = rows.find(r => r[0] === 'Mensagem');
      if (m) lines.push('', `Mensagem: ${m[1]}`);
      return lines.join('\n');
    }

    function validate(n) {
      if (n === 0) {
        const nome = form.elements.nome, tel = form.elements.telefone;
        nome.closest('.bfield').classList.toggle('is-invalid', val('nome').length < 2);
        const digits = val('telefone').replace(/\D/g, '');
        tel.closest('.bfield').classList.toggle('is-invalid', digits.length < 10);
        if (val('nome').length < 2) return 'Conte como podemos te chamar.';
        if (digits.length < 10) return 'Informe um WhatsApp com DDD, para a equipe retornar.';
        const em = val('email');
        if (em && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(em)) { form.elements.email.closest('.bfield').classList.add('is-invalid'); return 'Confira o e-mail ou deixe o campo em branco.'; }
        form.elements.email.closest('.bfield').classList.remove('is-invalid');
      }
      if (n === 1 && !sel('area').length) return 'Escolha pelo menos uma área (ou “Ainda não sei”).';
      if (n === 2 && !sel('objetivo').length && !val('outro')) return 'Marque pelo menos um objetivo ou escreva o seu.';
      if (n === 3) { if (!one('idade')) return 'Selecione a sua faixa etária.'; if (!one('acomp')) return 'Conte se você tem acompanhamento médico hoje.'; }
      if (n === 4 && !one('formato')) return 'Escolha o formato de atendimento.';
      if (n === 5 && !form.elements.consentimento.checked) return 'Para enviar, autorize o uso dos dados para o agendamento.';
      return '';
    }

    function render() {
      const f = first();
      root.querySelectorAll('[data-first]').forEach(e => { e.textContent = f ? `${f}, ` : ''; });
      root.querySelectorAll('[data-first-name]').forEach(e => { e.textContent = f ? `${f}!` : 'obrigada!'; });
      if (i === last) {
        root.querySelector('[data-summary]').innerHTML = data().map(([k, v]) => `<div><dt>${esc(k)}</dt><dd>${esc(v)}</dd></div>`).join('');
        root.querySelector('[data-preview]').textContent = message();
      }
    }

    function show(n, back) {
      steps.forEach((s, k) => { s.classList.toggle('is-active', k === n); s.classList.toggle('is-back', k === n && !!back); });
      done.classList.remove('is-active'); root.classList.remove('is-done');
      i = n; max = Math.max(max, n);
      bar.style.width = `${((n + 1) / steps.length) * 100}%`;
      num.textContent = String(n + 1).padStart(2, '0');
      prev.disabled = n === 0;
      nextLabel.textContent = n === last ? 'Enviar pelo WhatsApp' : 'Continuar';
      nextIcon.innerHTML = n === last ? waIcon : arrowIcon;
      lis.forEach((li, k) => { li.classList.toggle('is-current', k === n); li.classList.toggle('is-done', k < n || (k <= max && k !== n)); });
      if (aside) {
        aside.classList.add('is-swap');
        setTimeout(() => {
          const f = first();
          aTitle.textContent = n === 1 && f ? `Prazer, ${f}.` : ASIDE[n][0];
          aText.textContent = ASIDE[n][1];
          aside.classList.remove('is-swap');
        }, 220);
      }
      render();
      steps[n].querySelector('.berror').textContent = '';
      form.scrollTop = 0;
      if (root.classList.contains('booking--inline') && n > 0) {
        const top = root.getBoundingClientRect().top;
        if (top < 0 || top > w.innerHeight * .4) w.scrollTo({ top: w.scrollY + top - 110, behavior: reduce ? 'auto' : 'smooth' });
      }
    }

    function go() {
      const err = validate(i);
      const step = steps[i];
      if (err) {
        step.querySelector('.berror').textContent = err;
        step.classList.remove('shake'); void step.offsetWidth; step.classList.add('shake');
        return;
      }
      if (i < last) { show(i + 1); return; }
      url = `https://wa.me/${WA}?text=${encodeURIComponent(message())}`;
      w.open(url, '_blank', 'noopener');
      steps.forEach(s => s.classList.remove('is-active'));
      done.classList.add('is-active'); root.classList.add('is-done');
      root.querySelector('[data-wa-link]').href = url;
      lis.forEach(li => { li.classList.remove('is-current'); li.classList.add('is-done'); });
      if (aside) { aTitle.textContent = 'Até breve.'; aText.textContent = 'A equipe da Atthis vai retornar pelo WhatsApp para confirmar a sua consulta.'; }
    }

    next.addEventListener('click', go);
    prev.addEventListener('click', () => { if (i > 0) show(i - 1, true); });
    lis.forEach((li, k) => li.addEventListener('click', () => { if (k <= max && k !== i && !root.classList.contains('is-done')) show(k, k < i); }));
    form.addEventListener('submit', e => { e.preventDefault(); go(); });
    form.addEventListener('keydown', e => {
      if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA' && !e.isComposing) { e.preventDefault(); go(); }
    });

    /* máscara de telefone (DDD) 9XXXX-XXXX */
    const tel = form.elements.telefone;
    tel.addEventListener('input', () => {
      const v = tel.value.replace(/\D/g, '').slice(0, 11);
      let o = v;
      if (v.length > 2) o = `(${v.slice(0, 2)}) ${v.slice(2)}`;
      if (v.length > 7) o = `(${v.slice(0, 2)}) ${v.slice(2, v.length === 11 ? 7 : 6)}-${v.slice(v.length === 11 ? 7 : 6)}`;
      tel.value = o;
    });
    form.addEventListener('input', e => { const b = e.target.closest('.bfield'); if (b) b.classList.remove('is-invalid'); });

    /* campo condicional (familiar) e opções exclusivas (Nenhuma / Prefiro falar) */
    const cond = root.querySelector('[data-cond]');
    const syncCond = () => cond && cond.classList.toggle('is-shown', one(cond.dataset.cond) !== cond.dataset.condNot);
    form.addEventListener('change', e => {
      syncCond();
      const ex = e.target.closest('[data-exclusive]');
      if (ex && e.target.checked) {
        const only = ex.dataset.exclusive.split('|');
        const boxes = [...ex.querySelectorAll('input')];
        if (only.includes(e.target.value)) boxes.forEach(b => { if (b !== e.target) b.checked = false; });
        else boxes.forEach(b => { if (only.includes(b.value)) b.checked = false; });
      }
      const step = e.target.closest('.bstep'); if (step) step.querySelector('.berror').textContent = '';
    });
    syncCond();

    return {
      preset(area) {
        if (!area) return;
        form.querySelectorAll('[name="area"]').forEach(c => { if (c.value === area) c.checked = true; });
      },
      reset() { form.reset(); max = 0; syncCond(); show(0); },
      isDone: () => root.classList.contains('is-done'),
      focus() { const f = steps[i] && steps[i].querySelector('input:not([type=radio]):not([type=checkbox]), textarea'); if (f && w.innerWidth > 920) f.focus({ preventScroll: true }); },
      show
    };
  }

  const inline = d.querySelector('.booking--inline');
  if (inline) Booking(inline).show(0);

  const modal = d.querySelector('.booking:not(.booking--inline)');
  if (modal) {
    const bk = Booking(modal);
    bk.show(0);
    let lastFocus = null;
    const open = area => {
      if (inline) { /* na página de contato, leva até o formulário da página */
        const top = inline.getBoundingClientRect().top + w.scrollY - 110;
        w.scrollTo({ top, behavior: reduce ? 'auto' : 'smooth' });
        return;
      }
      if (bk.isDone()) bk.reset();
      bk.preset(area);
      lastFocus = d.activeElement;
      modal.classList.add('is-open');
      modal.setAttribute('aria-hidden', 'false');
      d.body.classList.add('booking-open');
      d.body.classList.remove('menu-open');
      setTimeout(() => bk.focus(), 450);
    };
    const close = () => {
      modal.classList.remove('is-open');
      modal.setAttribute('aria-hidden', 'true');
      d.body.classList.remove('booking-open');
      if (bk.isDone()) setTimeout(() => bk.reset(), 500);
      if (lastFocus) lastFocus.focus({ preventScroll: true });
    };
    d.addEventListener('click', e => {
      const t = e.target.closest('[data-agendar]');
      if (t) { e.preventDefault(); open(t.dataset.area); return; }
      if (e.target.closest('.booking:not(.booking--inline) [data-close]')) close();
    });
    d.addEventListener('keydown', e => {
      if (!modal.classList.contains('is-open')) return;
      if (e.key === 'Escape') close();
      if (e.key === 'Tab') { /* mantém o foco dentro do pop-up */
        const f = [...modal.querySelectorAll('button:not([disabled]), a[href], input, textarea')].filter(el => el.offsetParent !== null);
        if (!f.length) return;
        const a = f[0], z = f[f.length - 1];
        if (e.shiftKey && d.activeElement === a) { e.preventDefault(); z.focus(); }
        else if (!e.shiftKey && d.activeElement === z) { e.preventDefault(); a.focus(); }
      }
    });
    if (location.hash === '#agendar') open();
  }

  /* Ano no rodapé */
  d.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
