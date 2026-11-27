# -*- coding: utf-8 -*-
"""
Gerador do site Atthis — Dra. Aclair Dallagranna.

Todo o conteúdo (textos, imagens, especialidades, FAQ, blog, pré-agendamento) fica neste arquivo.
Para regenerar as páginas depois de editar:  python site-fonte/build.py
Saída: pasta ../site  (HTML estático; CSS e JS em site/assets)

Itens marcados com  VALIDAR  precisam de confirmação da Dra./cliente antes de publicar.
"""
import json
import os
from html import escape
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "site"))
R = ""  # prefixo relativo da página em construção (definido em page())

# ------------------------------------------------------------------ dados
BRAND = "Atthis"
DRA = "Dra. Aclair Dallagranna"
TITULO = "Médica de Família e Comunidade"
REG = "CRM-DF 18142 · RQE 15614 · RQE 20140"
CNPJ = "ATHIS MEDICINA LTDA · CNPJ 42.398.786/0001-97"
WA_NUM = "5561992831370"
WA_TXT = "(61) 99283-1370"
ADDRESS_1 = "SEPS 712/912, Ed. Via Brasil, Sala 313"
ADDRESS_2 = "Asa Sul, Brasília-DF · CEP 70360-510"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&destination=SEPS+712+912+Ed+Via+Brasil+Sala+313+Asa+Sul+Brasilia+DF"
MAPS_EMBED = "https://www.google.com/maps?q=SEPS+712%2F912+Ed.+Via+Brasil+Asa+Sul+Bras%C3%ADlia+DF&output=embed"
INSTAGRAM = "https://www.instagram.com/aclair.dallagranna/"
INSTA_HANDLE = "@aclair.dallagranna"

# Imagens.
#  - "local:..." = arquivo em site/assets/img (fotos REAIS da Dra., vindas da LP antiga)
#  - demais = fotos gratuitas do Unsplash (provisórias, carregadas por link)
IMG = {
    # Dra. Aclair — fotos reais
    "dra_retrato": "local:dra/dra-retrato.jpg",
    "dra_consultorio": "local:dra/dra-consultorio.jpg",
    "dra_largo": "local:dra/dra-consultorio-largo.jpg",
    "dra_avatar": "local:dra/dra-avatar.jpg",
    # Unsplash (provisórias)
    "familia": "1585813597616-63e881759e9d",
    "familia2": "1761257517090-05334392ca07",
    "familia_dourada": "1795154372275-f95ec7962c22",
    "casal": "1647913097114-5975d965a1ff",
    "casal_abraco": "1625690987114-86f5af994b49",
    "comida": "1567769541715-8c71fe49fd43",
    "comida2": "1613846594009-15e8fda0657e",
    "mulher_45": "1786999584308-271d8937786b",
    "mulher_grisalha": "1665327476806-2010a688e300",
    "mulher_campo": "1604872205488-6ad321550c28",
    "idosa_flores": "1717333943146-6b377d81b88f",
    "sono": "1758273239475-2eb6b706f157",
    "alongamento": "1589480562577-f262ad5f49ad",
    "alongamento2": "1627788587705-8c402afe7ccc",
    "tele": "1628645339131-0c39c7527856",
    "caderno": "1504542227056-9178533a9175",
    "oliveira": "1690994065552-6a35a0455ea2",
    "oliveira2": "1669967282206-8883f5becbf2",
    "eucalipto": "1512716679859-da19b4af9c38",
    "caminhada": "1785013905760-360244869d67",
    "caminhada2": "1759102701634-385d8b7e9f64",
    "cha_janela": "1545386673-7723f55e5490",
    "salvia": "1734367607096-9005870e78b7",
}


def u(key, w=1600, q=85):
    v = IMG[key]
    if v.startswith("local:"):
        return f"{R}assets/img/{v[6:]}"
    return f"https://images.unsplash.com/photo-{v}?auto=format&fit=crop&w={w}&q={q}"


def pic(key, alt, sizes="100vw", eager=False, pos=None, widths=(800, 1200, 1800, 2400)):
    style = f' style="object-position:{pos}"' if pos else ""
    load = 'eager" fetchpriority="high' if eager else "lazy"
    if IMG[key].startswith("local:"):
        return f'<img src="{u(key)}" alt="{escape(alt)}" loading="{load}" decoding="async"{style}>'
    srcset = ", ".join(f"{u(key, w)} {w}w" for w in widths)
    return (f'<img src="{u(key)}" srcset="{srcset}" sizes="{sizes}" alt="{escape(alt)}" '
            f'loading="{load}" decoding="async"{style}>')


# ------------------------------------------------------------------ ícones (traço uniforme, grade 24px)
P = {
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "chev": '<path d="m6 9 6 6 6-6"/>',
    "home": '<path d="M8.62 13.8A2.25 2.25 0 1 1 12 10.836a2.25 2.25 0 1 1 3.38 2.966l-2.626 2.856a.998.998 0 0 1-1.507 0z"/><path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>',
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/>',
    "pulse": '<path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.25.25 0 0 1-.48 0L9.24 2.18a.25.25 0 0 0-.48 0l-2.35 8.36A2 2 0 0 1 4.49 12H2"/>',
    "flower": '<circle cx="12" cy="12" r="3"/><path d="M12 16.5A4.5 4.5 0 1 1 7.5 12 4.5 4.5 0 1 1 12 7.5a4.5 4.5 0 1 1 4.5 4.5 4.5 4.5 0 1 1-4.5 4.5"/><path d="M12 7.5V9"/><path d="M7.5 12H9"/><path d="M16.5 12H15"/><path d="M12 16.5V15"/><path d="m8 8 1.88 1.88"/><path d="M14.12 9.88 16 8"/><path d="m8 16 1.88-1.88"/><path d="M14.12 14.12 16 16"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "scale": '<path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    "video": '<path d="m16 13 5.223 3.482a.5.5 0 0 0 .777-.416V7.87a.5.5 0 0 0-.752-.432L16 10.5"/><rect x="2" y="6" width="14" height="12" rx="2"/>',
    "pin": '<path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 14.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/>',
    "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "receipt": '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/>',
    "compass": '<path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z"/><circle cx="12" cy="12" r="10"/>',
    "loop": '<path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/>',
    "moon": '<path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/>',
    "heart": '<path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>',
    "check": '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>',
    "tick": '<path d="M20 6 9 17l-5-5"/>',
    "calendar": '<path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/>',
    "users": '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>',
    "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    "insta": '<rect width="20" height="20" x="2" y="2" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "brain": '<path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/><path d="M17.599 6.5a3 3 0 0 0 .399-1.375"/><path d="M6.003 5.125A3 3 0 0 0 6.401 6.5"/><path d="M3.477 10.896a4 4 0 0 1 .585-.396"/><path d="M19.938 10.5a4 4 0 0 1 .585.396"/><path d="M6 18a4 4 0 0 1-1.967-.516"/><path d="M19.967 17.484A4 4 0 0 1 18 18"/>',
    "bone": '<path d="M17 10c.7-.7 1.69 0 2.5 0a2.5 2.5 0 1 0 0-5 .5.5 0 0 1-.5-.5 2.5 2.5 0 1 0-5 0c0 .81.7 1.8 0 2.5l-7 7c-.7.7-1.69 0-2.5 0a2.5 2.5 0 0 0 0 5c.28 0 .5.22.5.5a2.5 2.5 0 1 0 5 0c0-.81-.7-1.8 0-2.5Z"/>',
    "syringe": '<path d="m18 2 4 4"/><path d="m17 7 3-3"/><path d="M19 9 8.7 19.3c-1 1-2.5 1-3.4 0l-.6-.6c-1-1-1-2.5 0-3.4L15 5"/><path d="m9 11 4 4"/><path d="m5 19-3 3"/><path d="m14 4 6 6"/>',
    "smile": '<circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><path d="M9 9h.01"/><path d="M15 9h.01"/>',
    "sparkle": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
    "lock": '<rect width="18" height="11" x="3" y="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><path d="M12 17h.01"/>',
    "x": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
}
WA_PATH = 'M17.47 14.38c-.3-.15-1.76-.87-2.03-.97-.27-.1-.47-.15-.67.15-.2.3-.77.97-.94 1.16-.17.2-.35.22-.64.08-.3-.15-1.26-.47-2.39-1.48-.88-.79-1.48-1.76-1.65-2.06-.17-.3-.02-.46.13-.6.13-.14.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.03-.52-.07-.15-.67-1.61-.92-2.2-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.79.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.21 3.07c.15.2 2.1 3.2 5.08 4.49.71.31 1.26.49 1.7.63.71.22 1.36.19 1.87.12.57-.09 1.76-.72 2-1.41.25-.7.25-1.29.17-1.41-.07-.13-.27-.2-.57-.35m-5.42 7.4h-.01a9.87 9.87 0 0 1-5.03-1.38l-.36-.21-3.74.98 1-3.65-.24-.37a9.86 9.86 0 0 1-1.5-5.26c0-5.45 4.43-9.88 9.89-9.88 2.64 0 5.12 1.03 6.99 2.9a9.82 9.82 0 0 1 2.89 6.99c0 5.45-4.44 9.88-9.89 9.88m8.41-18.3A11.82 11.82 0 0 0 12.05 0C5.5 0 .16 5.34.16 11.89c0 2.1.55 4.14 1.59 5.95L.06 24l6.3-1.65a11.88 11.88 0 0 0 5.68 1.45h.01c6.55 0 11.89-5.34 11.89-11.89a11.82 11.82 0 0 0-3.48-8.41Z'
WA_SVG = f'<svg class="wa-ic" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="{WA_PATH}"/></svg>'
STAR = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2c.6 5.2 4.8 9.4 10 10-5.2.6-9.4 4.8-10 10-.6-5.2-4.8-9.4-10-10 5.2-.6 9.4-4.8 10-10Z"/></svg>'


def ic(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{P[name]}</svg>'


def btn(label, href, kind="", icon="arrow", external=False, extra=""):
    k = f" btn--{kind}" if kind else ""
    tgt = ' target="_blank" rel="noopener"' if external else ""
    inner = WA_SVG if icon == "wa" else ic(icon)
    return f'<a class="btn{k}" href="{href}"{tgt}{extra}><span>{label}</span><span class="btn__icon">{inner}</span></a>'


def agendar(kind="", label="Agendar consulta", area=""):
    """Botão que abre o pop-up de pré-agendamento (em vez de ir direto ao WhatsApp)."""
    k = f" btn--{kind}" if kind else ""
    a = f' data-area="{escape(area)}"' if area else ""
    return f'<button type="button" class="btn{k}" data-agendar{a}><span>{label}</span><span class="btn__icon">{ic("calendar")}</span></button>'


def link_arrow(label, href, tag="a"):
    if tag == "span":
        return f'<span class="link-arrow">{label}{ic("arrow")}</span>'
    return f'<a class="link-arrow" href="{href}">{label}{ic("arrow")}</a>'


def wa(msg="Olá! Gostaria de agendar uma consulta com a Dra. Aclair Dallagranna."):
    return f"https://wa.me/{WA_NUM}?text={quote(msg)}"


# ------------------------------------------------------------------ especialidades
SPECS = [
    dict(
        slug="medicina-de-familia", name="Medicina de Família", icon="home",
        img="familia", pos="50% 35%",
        short="Um médico de referência que acompanha você, e a sua família, ao longo do tempo.",
        title="Um médico que conhece <em>você e a sua história.</em>",
        intro="A Medicina de Família e Comunidade é a especialidade do cuidado contínuo. Ela olha para a pessoa por inteiro, incluindo saúde física, emocional, rotina e contexto familiar, e acompanha cada fase da vida, coordenando o cuidado ao longo do tempo.",
        tags=["Cuidado contínuo", "Saúde integral", "Doenças crônicas", "Coordenação do cuidado"],
        para=[
            ("Quem quer um médico de referência", "Alguém que conhece seu histórico e acompanha sua saúde de perto."),
            ("Quem tem várias queixas ou condições", "Cuidado organizado e integrado, no lugar de consultas fragmentadas."),
            ("Quem convive com doenças crônicas", "Acompanhamento de hipertensão, diabetes e outras condições ao longo do tempo."),
            ("Famílias", "Atenção às diferentes fases da vida, com consultas individuais para cada pessoa."),
        ],
        como=[
            ("Escuta ampliada", "História de vida, rotina, contexto familiar e o que é importante para você."),
            ("Avaliação integral", "Revisão de sintomas, exames, medicamentos e fatores de risco."),
            ("Plano de cuidado", "Prioridades claras, metas realistas e prevenção adequada à sua idade e ao seu histórico."),
            ("Continuidade", "Retornos para acompanhar e ajustar o plano e, quando necessário, coordenar o cuidado com outros especialistas."),
        ],
        quote="Uma medicina que cuida da pessoa, não apenas da doença.",
        faq=["dif-mfc", "familia"],
    ),
    dict(
        slug="medicina-do-estilo-de-vida", name="Medicina do Estilo de Vida", icon="leaf",
        img="alongamento", pos="50% 40%",
        short="Hábitos como base do cuidado para prevenir e controlar doenças crônicas.",
        title="Hábitos são o cuidado <em>mais contínuo que existe.</em>",
        intro="A Medicina do Estilo de Vida usa evidências científicas para orientar mudanças de hábitos que ajudam a prevenir e controlar doenças crônicas, como diabetes, hipertensão e obesidade. O foco está em mudanças possíveis e sustentáveis, construídas com você.",
        tags=["Alimentação", "Atividade física", "Sono", "Manejo do estresse"],
        pilares=[
            ("leaf", "Alimentação", "Comida de verdade, prazer à mesa e escolhas que cabem na sua rotina."),
            ("pulse", "Movimento", "Atividade física adequada à sua condição, para força, disposição e saúde do coração."),
            ("moon", "Sono", "Uma rotina de sono que favorece energia, humor e equilíbrio metabólico."),
            ("sun", "Manejo do estresse", "Estratégias práticas para lidar com a sobrecarga do dia a dia."),
            ("heart", "Relações", "Vínculos, propósito e convivência como parte da saúde."),
            ("shield", "Substâncias", "Redução do tabaco, do excesso de álcool e de outros fatores de risco."),
        ],
        como=[
            ("Diagnóstico da rotina", "Entendemos como você come, se movimenta, dorme e lida com o estresse."),
            ("Prioridades possíveis", "Escolhemos juntos poucas mudanças, com maior impacto para a sua saúde."),
            ("Metas realistas", "Passos pequenos e mensuráveis, respeitando seu ritmo e sua vida real."),
            ("Acompanhamento", "Retornos para revisar o que funcionou, ajustar o plano e consolidar hábitos."),
        ],
        quote="Viver mais é consequência. Viver bem é escolha, e começa com pequenas ações.",
        faq=["atendimento", "primeira"],
    ),
    dict(
        slug="longevidade", name="Longevidade", icon="sun",
        img="casal", pos="50% 50%",
        short="Qualidade de vida ao longo dos anos, com autonomia, disposição e independência.",
        title="Viver mais é consequência. <em>Viver bem é escolha.</em>",
        intro="Longevidade, para nós, é qualidade de vida ao longo dos anos: preservar autonomia, disposição, memória e independência. Não se trata de prometer juventude, e sim de cuidar hoje da saúde que você quer ter amanhã.",
        tags=["Autonomia", "Funcionalidade", "Saúde cognitiva", "Prevenção"],
        para=[
            ("Adultos que querem envelhecer bem", "Planejar hoje os cuidados que fazem diferença nas próximas décadas."),
            ("Pessoas na meia-idade", "Mudanças metabólicas e hormonais, sono e bem-estar emocional."),
            ("Pessoas idosas", "Mobilidade, prevenção de quedas, doenças crônicas e preservação da independência."),
            ("Quem busca prevenção personalizada", "Exames e rastreamentos de acordo com idade, histórico e risco."),
        ],
        pilares=[
            ("pulse", "Força e mobilidade", "Massa muscular, equilíbrio e prevenção de quedas."),
            ("heart", "Saúde cardiometabólica", "Pressão, glicemia, colesterol e composição corporal."),
            ("brain", "Saúde cognitiva", "Memória, sono, estímulos e vínculos."),
            ("moon", "Sono e energia", "Descanso de qualidade como base para o dia a dia."),
            ("smile", "Saúde emocional", "Propósito, convivência e bem-estar."),
            ("shield", "Prevenção", "Rastreamentos e vacinas no tempo certo."),
        ],
        como=[
            ("Avaliação funcional e de risco", "Um retrato atual da sua saúde e dos fatores que mais pesam no seu futuro."),
            ("Plano de prevenção", "Prioridades definidas para a sua idade, o seu histórico e os seus objetivos."),
            ("Hábitos como tratamento", "Movimento, alimentação, sono e vínculos no centro do cuidado."),
            ("Acompanhamento ao longo do tempo", "Revisões periódicas para ajustar o plano a cada fase da vida."),
        ],
        quote="Cuidar hoje transforma o amanhã.",
        faq=["primeira", "exames"],
    ),
    dict(
        slug="emagrecimento-saudavel", name="Emagrecimento Saudável", icon="scale",
        img="comida", pos="50% 50%",
        short="Acompanhamento médico individualizado e ético, com foco em saúde metabólica.",
        title="Emagrecer é recuperar <em>o equilíbrio do corpo e da mente.</em>",
        intro="Um acompanhamento médico individualizado e ético para cuidar do peso com foco em saúde metabólica, composição corporal e hábitos sustentáveis. Sem dietas restritivas, sem fórmulas prontas e sem promessas rápidas.",
        tags=["Saúde metabólica", "Composição corporal", "Hábitos sustentáveis", "Acompanhamento"],
        para=[
            ("Quem já tentou várias dietas", "E busca uma abordagem sustentável, sem restrições extremas."),
            ("Quem tem alterações metabólicas", "Como mudanças na glicemia, no colesterol ou na pressão arterial."),
            ("Quem quer cuidar do peso com segurança", "Com acompanhamento médico próximo e avaliação completa."),
            ("Quem passa por mudanças hormonais", "Como na meia-idade e na menopausa."),
        ],
        como=[
            ("Avaliação completa", "Histórico, exames, sono, estresse, medicamentos e rotina."),
            ("Metas realistas", "Definidas com você, respeitando seu ritmo e sua vida real."),
            ("Plano individualizado", "Alimentação, movimento e sono e, quando indicado, tratamento individualizado após avaliação médica."),
            ("Acompanhamento contínuo", "Retornos para ajustar o plano e consolidar os novos hábitos."),
        ],
        notice="Cada pessoa responde de forma diferente. Não há promessa de perda de peso, prazo ou resultado garantido.",
        quote="Emagrecer é mais que perder peso: é recuperar o equilíbrio do corpo e da mente.",
        faq=["emagrecimento", "primeira"],
    ),
    dict(
        slug="saude-da-mulher", name="Saúde da Mulher", icon="flower",
        img="mulher_45", pos="50% 30%",
        short="Cuidado individualizado em todas as fases, da contracepção à menopausa.",
        title="Cuidado em cada fase, <em>da contracepção à menopausa.</em>",
        intro="Acompanhamento médico individualizado para todas as etapas da vida da mulher, com escuta, informação de qualidade e decisões compartilhadas.",
        tags=["Contracepção", "Prevenção", "Meia-idade", "Menopausa"],
        pilares=[
            ("calendar", "Contracepção e planejamento", "Orientação sobre métodos contraceptivos, incluindo o DIU."),
            ("shield", "Rastreamentos preventivos", "Exames de acordo com a idade e o histórico."),
            ("flower", "Climatério e menopausa", "Sintomas, sono, humor e qualidade de vida."),
            ("bone", "Saúde óssea e cardiovascular", "Prevenção na meia-idade e depois dela."),
            ("smile", "Saúde emocional", "Atenção ao bem-estar em cada fase."),
            ("pulse", "Metabolismo e peso", "Mudanças na composição corporal ao longo da vida."),
        ],
        como=[
            ("Escuta e informação", "Tempo para suas dúvidas e explicações claras sobre cada opção."),
            ("Decisões compartilhadas", "Você participa das escolhas sobre o seu cuidado."),
            ("Prevenção ao longo da vida", "Rastreamentos e cuidados adequados a cada fase."),
            ("Acompanhamento contínuo", "Retornos para acompanhar mudanças e ajustar o cuidado."),
        ],
        quote="Informação e acompanhamento para viver cada fase com mais segurança.",
        faq=["primeira", "convenio"],
    ),
    dict(
        slug="medicina-preventiva", name="Medicina Preventiva", icon="shield",
        img="caminhada", pos="50% 50%",
        short="Exames, rastreamentos e hábitos definidos para o seu momento de vida.",
        title="O melhor cuidado é <em>o que começa antes.</em>",
        intro="Prevenção personalizada: exames, rastreamentos e hábitos definidos de acordo com a sua idade, o seu histórico e os seus fatores de risco. Sem excesso de exames e sem deixar de lado o que é importante.",
        tags=["Check-up individualizado", "Rastreamentos", "Fatores de risco", "Vacinação do adulto"],
        pilares=[
            ("check", "Check-up individualizado", "Exames escolhidos para você, e não um pacote padrão."),
            ("shield", "Rastreamentos", "Câncer, doenças cardiovasculares e diabetes, conforme as recomendações para cada idade."),
            ("heart", "Fatores de risco", "Pressão, colesterol, glicemia, peso, tabagismo e sedentarismo."),
            ("syringe", "Vacinação do adulto", "Orientação sobre as vacinas indicadas em cada fase."),
            ("loop", "Doenças crônicas", "Acompanhamento para prevenir complicações."),
            ("leaf", "Hábitos", "O estilo de vida como principal ferramenta de prevenção."),
        ],
        como=[
            ("Avaliação de risco", "Histórico pessoal e familiar, hábitos e exames anteriores."),
            ("Plano preventivo", "O que fazer, quando fazer e por quê, explicado com clareza."),
            ("Orientação prática", "Hábitos e cuidados que cabem na sua rotina."),
            ("Revisão periódica", "O plano acompanha você e muda conforme a idade e o momento de vida."),
        ],
        quote="Prevenir é a forma mais cuidadosa de cuidar.",
        faq=["exames", "atendimento"],
    ),
]

# ------------------------------------------------------------------ FAQ
FAQ = {
    "atendimento": ("Como funciona o atendimento?",
        "O atendimento pode ser presencial, no consultório na Asa Sul, em Brasília, ou por telemedicina. Na primeira consulta fazemos uma avaliação completa do seu histórico de saúde, dos seus hábitos de vida e dos seus objetivos. A partir dela, construímos juntos um plano de cuidado personalizado, com acompanhamento contínuo."),
    "primeira": ("O que esperar da primeira consulta?",
        "Uma conversa sem pressa. Revisamos sua história, seus exames, sua rotina e o que é importante para você. O objetivo é entender o todo, e não apenas um sintoma isolado, para definir prioridades e próximos passos."),
    "duracao": ("Quanto tempo dura uma consulta?",
        "As consultas têm duração média de 60 minutos."),
    "exames": ("Preciso levar exames?",
        "Se tiver exames recentes, leve-os (ou envie antes da teleconsulta), junto com a lista de medicamentos e suplementos que você usa. Se for necessário, novos exames serão solicitados de forma individualizada."),
    "tele": ("Como funciona a consulta por telemedicina?",
        "No dia e horário marcados você recebe o link da videoconferência. Recomendamos um ambiente tranquilo, com boa conexão, e ter em mãos seus exames recentes e a lista de medicamentos em uso."),
    "convenio": ("Atende por convênio?",
        "Os atendimentos são particulares. Fornecemos recibo para que você solicite reembolso ao seu convênio, quando aplicável."),
    "familia": ("Pessoas da mesma família podem se consultar?",
        "Sim. As consultas são individuais, e o atendimento de mais de uma pessoa da família pode ser organizado no momento do agendamento."),
    "agendar": ("Como posso agendar?",
        "Pelo pré-agendamento do site: em poucos passos você conta o que procura, e a mensagem chega pronta no WhatsApp da equipe, que retorna para confirmar dia, horário e formato."),
    "dif-mfc": ("Qual a diferença entre médico de família e clínico geral?",
        "A Medicina de Família e Comunidade é uma especialidade médica, com formação específica (residência ou especialização de dois anos), voltada ao cuidado contínuo da pessoa em todas as fases da vida, considerando também o contexto familiar e social. O médico de família acompanha você ao longo do tempo e coordena o cuidado, inclusive quando é preciso envolver outros especialistas."),
    "vida": ("O que é o Programa Vida Atthis?",
        "É o programa de acompanhamento da Atthis: um plano de 6 meses para saúde integral. As etapas são apresentadas na consulta, de acordo com as suas necessidades."),
    "emagrecimento": ("O acompanhamento para emagrecer usa medicamentos?",
        "Cada caso é avaliado individualmente. Quando há indicação, o tratamento é definido após avaliação médica, sempre junto com mudanças de hábitos sustentáveis. Não trabalhamos com promessas de resultado nem com fórmulas prontas."),
}
FAQ_HOME = ["atendimento", "primeira", "dif-mfc", "tele", "convenio"]
FAQ_GROUPS = [
    ("Consultas", ["atendimento", "primeira", "duracao", "exames"]),
    ("Atendimento e agendamento", ["agendar", "tele", "convenio", "familia"]),
    ("Especialidade e programas", ["dif-mfc", "vida", "emagrecimento"]),
]


def faq_html(keys):
    items = []
    for k in keys:
        q, a = FAQ[k]
        items.append(f'<details><summary>{q}<i aria-hidden="true"></i></summary><div class="faq__a"><p>{a}</p></div></details>')
    return '<div class="faq">' + "".join(items) + "</div>"


# ------------------------------------------------------------------ blog
POSTS = [
    dict(slug="longevidade-e-qualidade-de-vida", title="Longevidade é qualidade de vida, não só mais anos",
         cat="longevidade", catname="Longevidade", img="casal_abraco", pos="50% 40%", min=6,
         excerpt="O que realmente significa envelhecer bem e quais hábitos fazem diferença ao longo das décadas."),
    dict(slug="longevidade-e-qualidade-de-vida", title="Médico de família ou clínico geral: qual a diferença?",
         cat="familia", catname="Medicina de Família", img="familia2", pos="50% 40%", min=4,
         excerpt="Entenda o papel do médico de família e por que ter um médico de referência faz diferença."),
    dict(slug="longevidade-e-qualidade-de-vida", title="Sono e metabolismo: o que um tem a ver com o outro",
         cat="estilo", catname="Estilo de vida", img="sono", pos="50% 40%", min=5,
         excerpt="Dormir mal afeta apetite, energia e glicemia. Veja como o sono entra no cuidado com a saúde."),
    dict(slug="longevidade-e-qualidade-de-vida", title="Menopausa: o que muda no corpo e como se cuidar",
         cat="mulher", catname="Saúde da Mulher", img="mulher_grisalha", pos="50% 30%", min=7,
         excerpt="Sintomas, sono, humor, ossos e coração: um guia para atravessar essa fase com informação."),
    dict(slug="longevidade-e-qualidade-de-vida", title="Emagrecer com saúde: por que o acompanhamento faz diferença",
         cat="emagrecimento", catname="Emagrecimento", img="comida2", pos="50% 50%", min=5,
         excerpt="Sem fórmulas prontas: o que considerar para cuidar do peso de forma segura e sustentável."),
    dict(slug="longevidade-e-qualidade-de-vida", title="Check-up: o que realmente faz sentido para a sua idade",
         cat="prevencao", catname="Prevenção", img="caminhada2", pos="50% 50%", min=6,
         excerpt="Mais exames não significa mais saúde. Como funciona a prevenção individualizada."),
    dict(slug="longevidade-e-qualidade-de-vida", title="Força muscular: uma aliada da autonomia ao longo dos anos",
         cat="longevidade", catname="Longevidade", img="alongamento2", pos="50% 50%", min=5,
         excerpt="Por que cuidar da massa muscular é uma das melhores formas de preservar a independência."),
]


def post_card(p, r):
    return (f'<a class="post-card" href="{r}blog/{p["slug"]}.html" data-cat="{p["cat"]}">'
            f'<div class="post-card__img">{pic(p["img"], p["title"], "(max-width: 600px) 100vw, 33vw", pos=p["pos"], widths=(600, 900, 1300))}</div>'
            f'<div class="post-card__meta"><span class="tag">{p["catname"]}</span><span>{p["min"]} min de leitura</span></div>'
            f'<h3 class="h3">{p["title"]}</h3><p>{p["excerpt"]}</p></a>')


# ------------------------------------------------------------------ pré-agendamento (pop-up + versão na página de contato)
BK_AREAS = [(s["name"], s["icon"], s["short"]) for s in SPECS] + [
    ("Programa Vida Atthis", "sparkle", "Acompanhamento de 6 meses para saúde integral."),
    ("Ainda não sei", "help", "Quero uma avaliação geral para entender por onde começar."),
]
BK_OBJETIVOS = ["Prevenir doenças", "Ter mais energia", "Dormir melhor", "Cuidar do peso", "Melhorar a alimentação",
                "Começar a me exercitar", "Controlar pressão, glicemia ou colesterol", "Passar bem pela menopausa",
                "Envelhecer com autonomia", "Fazer um check-up", "Reduzir o estresse", "Organizar exames e medicamentos"]
BK_IDADE = ["Até 29", "30 a 39", "40 a 49", "50 a 59", "60 a 69", "70 ou mais"]
BK_ACOMP = ["Sim, regularmente", "Às vezes", "Não, há algum tempo"]
BK_COND = ["Hipertensão", "Diabetes ou pré-diabetes", "Colesterol alterado", "Tireoide", "Ansiedade ou depressão",
           "Nenhuma", "Prefiro falar na consulta"]
BK_PERIODO = ["Manhã", "Tarde", "Qualquer horário"]
BK_ORIGEM = ["Instagram", "Google", "Indicação", "Já sou paciente", "Outro"]
BK_STEPS = ["Você", "Motivo", "Objetivos", "Saúde", "Preferências", "Revisão"]


def _opts(name, values, multi=False, checked=None):
    t = "checkbox" if multi else "radio"
    return "".join(
        f'<label class="bopt"><input type="{t}" name="{name}" value="{escape(v)}"{" checked" if v == checked else ""}><span>{v}</span></label>'
        for v in values)


def booking(r, p="m", inline=False):
    tick = ic("tick")
    areas = "".join(
        f'<label class="bcard"><input type="checkbox" name="area" value="{escape(n)}"><span class="bcard__tick">{tick}</span>'
        f'<span class="bcard__in"><span class="bcard__ic">{ic(i)}</span><span><strong>{n}</strong><small>{s}</small></span></span></label>'
        for n, i, s in BK_AREAS)
    fmt = (f'<label class="bcard"><input type="radio" name="formato" value="Presencial (Asa Sul, Brasília)"><span class="bcard__tick">{tick}</span>'
           f'<span class="bcard__in"><span class="bcard__ic">{ic("pin")}</span><span><strong>Presencial</strong><small>Consultório na Asa Sul, Brasília.</small></span></span></label>'
           f'<label class="bcard"><input type="radio" name="formato" value="Telemedicina"><span class="bcard__tick">{tick}</span>'
           f'<span class="bcard__in"><span class="bcard__ic">{ic("video")}</span><span><strong>Telemedicina</strong><small>De onde você estiver, por vídeo.</small></span></span></label>'
           f'<label class="bcard"><input type="radio" name="formato" value="Sem preferência"><span class="bcard__tick">{tick}</span>'
           f'<span class="bcard__in"><span class="bcard__ic">{ic("compass")}</span><span><strong>Tanto faz</strong><small>Combinamos o melhor formato.</small></span></span></label>')
    steps_aside = "".join(f'<li data-goto="{k}"><i></i><span>{n}</span></li>' for k, n in enumerate(BK_STEPS))
    cls = "booking booking--inline" if inline else "booking"
    role = '' if inline else ' role="dialog" aria-modal="true" aria-hidden="true"'
    return f'''
<div class="{cls}" id="{"pre-agendamento" if inline else "agendamento"}"{role} aria-labelledby="{p}-title">
  <div class="booking__backdrop" data-close></div>
  <div class="booking__panel">
    <aside class="booking__aside texture">
      <img class="booking__logo" src="{r}assets/img/logo-atthis-completo-claro.svg" alt="{BRAND}">
      <img class="booking__fly" src="{r}assets/img/libelula-claro.png" alt="">
      <div class="booking__intro">
        <p class="eyebrow">Pré-agendamento</p>
        <h2 class="booking__title" id="{p}-title" data-aside-title>Vamos cuidar de você.</h2>
        <p data-aside-text>Em poucos passos, a Dra. Aclair entende o que você busca antes mesmo da primeira conversa.</p>
      </div>
      <ol class="booking__steps">{steps_aside}</ol>
      <p class="booking__lgpd">{ic("lock")}<span>Seus dados são usados apenas para o agendamento.</span></p>
    </aside>
    <div class="booking__main">
      <header class="booking__top">
        <span class="booking__count"><b data-step-num>01</b> / 0{len(BK_STEPS)}</span>
        <div class="booking__bar"><i data-bar></i></div>
        <button type="button" class="booking__close" data-close aria-label="Fechar">{ic("x")}</button>
      </header>
      <form class="booking__form" novalidate>
        <section class="bstep is-active" data-step="0">
          <p class="bstep__kicker">Etapa 1 · Apresentação</p>
          <h3 class="bstep__q">Para começar, <em>como podemos te chamar?</em></h3>
          <p class="bstep__hint">Leva menos de 2 minutos. Ao final, a mensagem chega pronta no WhatsApp da equipe.</p>
          <div class="bfield"><input id="{p}-nome" name="nome" placeholder=" " autocomplete="name" required><label for="{p}-nome">Seu nome</label></div>
          <div class="bgrid2">
            <div class="bfield"><input id="{p}-tel" name="telefone" type="tel" inputmode="tel" placeholder=" " autocomplete="tel" required><label for="{p}-tel">WhatsApp com DDD</label></div>
            <div class="bfield"><input id="{p}-email" name="email" type="email" placeholder=" " autocomplete="email"><label for="{p}-email">E-mail (opcional)</label></div>
          </div>
          <p class="blabel">A consulta é para</p>
          <div class="bchips">{_opts("para", ["Mim", "Um familiar", "Mim e minha família"], checked="Mim")}</div>
          <div class="bfield bcond" data-cond="para" data-cond-not="Mim"><input id="{p}-fam" name="familiar" placeholder=" "><label for="{p}-fam">Nome e idade do familiar (opcional)</label></div>
          <p class="berror" aria-live="polite"></p>
        </section>

        <section class="bstep" data-step="1">
          <p class="bstep__kicker">Etapa 2 · Motivo</p>
          <h3 class="bstep__q"><span data-first></span>o que te traz <em>até a Atthis?</em></h3>
          <p class="bstep__hint">Escolha uma ou mais áreas. Se não tiver certeza, marque “Ainda não sei”.</p>
          <div class="bcards">{areas}</div>
          <p class="berror" aria-live="polite"></p>
        </section>

        <section class="bstep" data-step="2">
          <p class="bstep__kicker">Etapa 3 · Objetivos</p>
          <h3 class="bstep__q">Quais são os seus <em>principais objetivos?</em></h3>
          <p class="bstep__hint">Marque quantos quiser. Eles ajudam a Dra. a preparar a sua primeira consulta.</p>
          <div class="bchips">{_opts("objetivo", BK_OBJETIVOS, multi=True)}</div>
          <div class="bfield" style="margin-top:18px"><input id="{p}-outro" name="outro" placeholder=" "><label for="{p}-outro">Outro objetivo (opcional)</label></div>
          <p class="berror" aria-live="polite"></p>
        </section>

        <section class="bstep" data-step="3">
          <p class="bstep__kicker">Etapa 4 · Sobre você</p>
          <h3 class="bstep__q">Um retrato <em>inicial da sua saúde.</em></h3>
          <p class="bstep__hint">Informações gerais. Os detalhes clínicos ficam para a consulta, em ambiente seguro.</p>
          <p class="blabel">Faixa etária</p>
          <div class="bchips">{_opts("idade", BK_IDADE)}</div>
          <p class="blabel">Você faz acompanhamento médico regular hoje?</p>
          <div class="bchips">{_opts("acomp", BK_ACOMP)}</div>
          <p class="blabel">Alguma condição já diagnosticada? <span class="opt">(opcional)</span></p>
          <div class="bchips" data-exclusive="Nenhuma|Prefiro falar na consulta">{_opts("condicao", BK_COND, multi=True)}</div>
          <p class="berror" aria-live="polite"></p>
        </section>

        <section class="bstep" data-step="4">
          <p class="bstep__kicker">Etapa 5 · Preferências</p>
          <h3 class="bstep__q">Como você prefere <em>o seu atendimento?</em></h3>
          <div class="bcards bcards--3" style="margin-top:22px">{fmt}</div>
          <p class="blabel">Melhor período para a equipe falar com você</p>
          <div class="bchips">{_opts("periodo", BK_PERIODO, checked="Qualquer horário")}</div>
          <p class="blabel">Como conheceu a Atthis? <span class="opt">(opcional)</span></p>
          <div class="bchips">{_opts("origem", BK_ORIGEM)}</div>
          <div class="bfield" style="margin-top:22px"><textarea id="{p}-msg" name="mensagem" placeholder=" " rows="3"></textarea><label for="{p}-msg">Algo que a Dra. Aclair deva saber antes do contato? (opcional)</label></div>
          <p class="berror" aria-live="polite"></p>
        </section>

        <section class="bstep" data-step="5">
          <p class="bstep__kicker">Etapa 6 · Revisão</p>
          <h3 class="bstep__q">Tudo pronto, <em data-first-name>obrigada!</em></h3>
          <p class="bstep__hint">Confira as informações. Ao enviar, o WhatsApp abre com esta mensagem pronta para a equipe.</p>
          <div class="breview">
            <dl class="bsummary" data-summary></dl>
            <div class="bwa">
              <div class="bwa__head"><img src="{r}assets/img/dra/dra-avatar.jpg" alt=""><div><strong>Atthis · Dra. Aclair</strong><small>Prévia da mensagem</small></div></div>
              <div class="bwa__bubble" data-preview></div>
            </div>
          </div>
          <label class="bconsent"><input type="checkbox" name="consentimento"><span>Autorizo o envio destas informações pelo WhatsApp para fins de agendamento, conforme a LGPD.</span></label>
          <p class="bnote">{ic("info")}<span>Em caso de urgência ou emergência, procure um pronto-atendimento ou ligue 192.</span></p>
          <p class="berror" aria-live="polite"></p>
        </section>

        <section class="bstep bdone" data-step="done">
          <svg viewBox="0 0 120 120" aria-hidden="true"><circle cx="60" cy="60" r="54" fill="none" stroke="#a59267" stroke-width="1.5"/><path d="M38 61l15 15 30-32" fill="none" stroke="#4e6353" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>
          <h3 class="bstep__q">Mensagem <em>pronta!</em></h3>
          <p class="bstep__hint">Abrimos o WhatsApp com o seu pré-agendamento. É só tocar em <strong>enviar</strong>. A equipe da Atthis retorna para confirmar o dia, o horário e o formato.</p>
          <div class="btn-row" style="justify-content:center">
            <a class="btn" data-wa-link href="{wa()}" target="_blank" rel="noopener"><span>Abrir o WhatsApp</span><span class="btn__icon">{WA_SVG}</span></a>
            {"" if inline else f'<button type="button" class="btn btn--ghost" data-close><span>Fechar</span><span class="btn__icon">{ic("x")}</span></button>'}
          </div>
        </section>
      </form>
      <footer class="booking__nav">
        <button type="button" class="booking__back" data-prev>{ic("arrow")}Voltar</button>
        <span class="booking__key">Pressione <kbd>Enter</kbd> para continuar</span>
        <button type="button" class="btn" data-next><span data-next-label>Continuar</span><span class="btn__icon" data-next-icon>{ic("arrow")}</span></button>
      </footer>
    </div>
  </div>
</div>'''


# ------------------------------------------------------------------ layout
NAV = [
    ("index.html", "Início"),
    ("sobre.html", "A médica"),
    ("especialidades.html", "Especialidades"),
    ("como-funciona.html", "Como funciona"),
    ("blog.html", "Blog"),
    ("faq.html", "Dúvidas"),
    ("contato.html", "Contato"),
]


def header(r, active):
    links = []
    for href, label in NAV:
        cur = ' aria-current="page"' if href == active else ""
        if href == "especialidades.html":
            mega = "".join(
                f'<a href="{r}especialidades/{s["slug"]}.html"><span class="mega__ic">{ic(s["icon"])}</span>'
                f'<span class="mega__txt"><strong>{s["name"]}</strong><span>{s["short"]}</span></span></a>' for s in SPECS)
            mega += f'<a class="mega__all link-arrow" href="{r}especialidades.html">Ver todas as especialidades {ic("arrow")}</a>'
            links.append(f'<div class="nav__item"><a class="nav__link" href="{r}{href}"{cur}>{label}{ic("chev")}</a>'
                         f'<div class="mega">{mega}</div></div>')
        else:
            links.append(f'<a class="nav__link" href="{r}{href}"{cur}>{label}</a>')
    mobile = "".join(
        f'<a href="{r}{h}" style="--i:{i}">{l if h != "index.html" else "<em>Início</em>"}</a>' for i, (h, l) in enumerate(NAV))
    return f'''
<header class="site-header">
  <div class="container site-header__inner">
    <a class="brand" href="{r}index.html" aria-label="{BRAND}, página inicial"><img src="{r}assets/img/logo-atthis-completo.svg" alt="{BRAND}: Gestão personalizada da saúde. Cuidar hoje transforma o amanhã." width="562" height="280"></a>
    <nav class="nav" aria-label="Principal">{"".join(links)}</nav>
    <div class="header-cta">
      {agendar(label='Agendar<span class="txt-long"> consulta</span>')}
      <button class="nav-toggle" aria-label="Abrir menu" aria-expanded="false"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="mobile-menu" aria-label="Menu">
  <nav>{mobile}</nav>
  <div class="mobile-menu__foot">
    {agendar()}
    <span class="muted small">{ADDRESS_1} · {ADDRESS_2}</span>
    <span class="muted small">WhatsApp {WA_TXT} · {INSTA_HANDLE}</span>
  </div>
</div>'''


def footer(r):
    spec_links = "".join(f'<li><a href="{r}especialidades/{s["slug"]}.html">{s["name"]}</a></li>' for s in SPECS)
    nav_links = "".join(f'<li><a href="{r}{h}">{l}</a></li>' for h, l in NAV)
    return f'''
<footer class="site-footer texture">
  <div class="container">
    <div class="footer-top">
      <div class="footer-brand">
        <img src="{r}assets/img/logo-atthis-completo-claro.svg" alt="{BRAND}: Gestão personalizada da saúde. Cuidar hoje transforma o amanhã." width="562" height="280" loading="lazy">
        <p>Cuidado contínuo, preventivo e individualizado, em todas as fases da vida.</p>
      </div>
      <div><h4>Navegação</h4><ul>{nav_links}</ul></div>
      <div><h4>Especialidades</h4><ul>{spec_links}</ul></div>
      <div><h4>Contato</h4><ul class="footer-contact">
        <li>{ic("pin")}<a href="{MAPS_DIR}" target="_blank" rel="noopener">{ADDRESS_1}<br>{ADDRESS_2}</a></li>
        <li>{ic("phone")}<button type="button" class="footer-link" data-agendar>WhatsApp {WA_TXT}</button></li>
        <li>{ic("insta")}<a href="{INSTAGRAM}" target="_blank" rel="noopener">{INSTA_HANDLE}</a></li>
        <li>{ic("video")}<span>Presencial e telemedicina</span></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <span>Responsável técnica: <strong>{DRA}</strong> · {TITULO} · {REG}</span>
      <span>© <span data-year>2026</span> {BRAND} · {CNPJ}</span>
      <span>Conteúdo informativo. Não substitui a consulta médica.</span>
    </div>
  </div>
</footer>
<button type="button" class="wa-float" data-agendar aria-label="Agendar consulta">{ic("calendar")}<span>Agendar consulta</span></button>'''


def page(path, title, desc, body, active="", jsonld=None):
    global R
    depth = path.count("/")
    r = "../" * depth
    R = r
    full_title = f"{title} | {BRAND} · {DRA}" if path != "index.html" else f"{BRAND} · {DRA} | {TITULO} em Brasília"
    ld = f'<script type="application/ld+json">{json.dumps(jsonld, ensure_ascii=False)}</script>' if jsonld else ""
    content = body(r)
    html = f'''<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{escape(full_title)}</title>
<meta name="description" content="{escape(desc)}">
<meta name="theme-color" content="#4e6353">
<meta property="og:type" content="website">
<meta property="og:title" content="{escape(full_title)}">
<meta property="og:description" content="{escape(desc)}">
<meta property="og:image" content="{r}assets/img/dra/dra-retrato.jpg">
<meta property="og:locale" content="pt_BR">
<link rel="icon" type="image/png" href="{r}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400;1,500&family=Lato:wght@300;400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{r}assets/css/style.css">
{ld}
</head>
<body>
{header(r, active)}
<main id="conteudo">
{content}
</main>
{footer(r)}
{booking(r, "m")}
<script src="{r}assets/js/main.js" defer></script>
</body>
</html>
'''
    dest = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    print("ok", path)


# ------------------------------------------------------------------ blocos reutilizáveis
def cta_block(r, title="Sua saúde merece <em>tempo, escuta e continuidade.</em>"):
    return f'''
<section class="section" style="padding-bottom:0">
  <div class="container">
    <div class="cta texture" data-reveal>
      <img class="cta__dragonfly" src="{r}assets/img/libelula.png" alt="">
      <div>
        <p class="eyebrow">Agendamento</p>
        <h2 class="title">{title}</h2>
      </div>
      <div class="cta__side">
        {agendar(label="Fazer pré-agendamento")}
        {btn("Outras formas de contato", f"{r}contato.html", "ghost")}
        <p>{ADDRESS_1} · {ADDRESS_2}<br>Presencial ou por telemedicina</p>
      </div>
    </div>
  </div>
</section>'''


def program_block(r):
    return f'''
<section class="section section--olive texture" id="vida-atthis">
  <div class="container program">
    <div class="program__badge" data-reveal="fade">
      <svg viewBox="0 0 560 320" role="img" aria-label="Programa Vida Atthis">
        <g fill="none" stroke="#cbbd99" stroke-width="1.4" stroke-linecap="round">
          <path class="draw" d="M92 160 A130 130 0 0 1 222 30 H338 A130 130 0 0 1 468 160"/>
          <path class="draw" d="M98 196 A130 130 0 0 0 222 290 H338 A130 130 0 0 0 456 214"/>
        </g>
        <circle cx="474" cy="168" r="9" fill="#d4c6a2"/>
        <path fill="#d4c6a2" d="M60 132c2.2 16 11 25.8 27 28-16 2.2-24.8 12-27 28-2.2-16-11-25.8-27-28 16-2.2 24.8-12 27-28Z"/>
        <text x="280" y="148" text-anchor="middle" font-family="Cormorant Garamond, serif" font-weight="300" font-size="64" letter-spacing="10" fill="#e8dfd1">VIDA</text>
        <text x="280" y="226" text-anchor="middle" font-family="Cormorant Garamond, serif" font-weight="300" font-size="64" letter-spacing="10" fill="#e8dfd1">ATTHIS</text>
      </svg>
      <div class="quote-sign" data-reveal>
        <img src="{r}assets/img/dra/dra-avatar.jpg" alt="{DRA}">
        <p class="quote-line">“Toda grande transformação começa com uma pequena decisão.”<small>{DRA}</small></p>
      </div>
    </div>
    <div>
      <p class="eyebrow" data-reveal>Programa de acompanhamento</p>
      <h2 class="title" data-reveal>Seis meses para cuidar da sua saúde <em>por inteiro.</em></h2>
      <p class="lead" data-reveal style="margin-top:26px">O Vida Atthis é o programa de acompanhamento da Atthis: um plano de 6 meses para saúde integral, com avaliação, prioridades definidas em conjunto e acompanhamento próximo ao longo do caminho.</p>
      <!-- VALIDAR: etapas e o que o programa inclui (não recebido). Texto abaixo é genérico. -->
      <ul class="program__list" data-stagger>
        <li><b>i.</b><div><strong>Avaliação inicial completa</strong><span>Histórico, hábitos, exames e objetivos.</span></div></li>
        <li><b>ii.</b><div><strong>Plano individualizado</strong><span>Metas realistas e prioridades claras para os seis meses.</span></div></li>
        <li><b>iii.</b><div><strong>Acompanhamento contínuo</strong><span>Retornos e ajustes ao longo de todo o programa.</span></div></li>
      </ul>
      <div class="btn-row" data-reveal>{agendar("light", "Quero conhecer o programa", "Programa Vida Atthis")}</div>
    </div>
  </div>
</section>'''


def exp_block(r, head=True):
    h = f'''
    <div class="sec-head">
      <div><p class="eyebrow" data-reveal>Experiência do paciente</p>
      <h2 class="title" data-reveal>Tempo, escuta e <em>um plano que é seu.</em></h2></div>
      <p class="lead" data-reveal>Cada consulta é pensada para entender o todo: sua história, sua rotina e o que é importante para você. Sem pressa e com explicações claras.</p>
    </div>''' if head else ""
    return f'''
<section class="section section--mist texture">
  <div class="container">{h}
    <div class="exp" data-stagger>
      <div class="exp__item"><div class="exp__ic">{ic("clock")}</div><h3 class="h3">Tempo para ouvir</h3><p>Consultas com duração média de 60 minutos, para entender sua história e seus objetivos.</p></div>
      <div class="exp__item"><div class="exp__ic">{ic("compass")}</div><h3 class="h3">Avaliação individualizada</h3><p>Histórico, rotina, exames e contexto de vida analisados em conjunto.</p></div>
      <div class="exp__item"><div class="exp__ic">{ic("chat")}</div><h3 class="h3">Plano construído junto</h3><p>Metas realistas e um plano de cuidado feito para a sua vida real.</p></div>
      <div class="exp__item"><div class="exp__ic">{ic("loop")}</div><h3 class="h3">Acompanhamento contínuo</h3><p>Retornos e ajustes ao longo do tempo, e não uma consulta isolada.</p></div>
    </div>
    <div class="info-bar" data-stagger>
      <div class="info-bar__item">{ic("pin")}<div><strong>Presencial ou online</strong><span>Consultório na Asa Sul ou telemedicina</span></div></div>
      <div class="info-bar__item">{ic("receipt")}<div><strong>Atendimento particular</strong><span>Recibo para reembolso do convênio, quando aplicável</span></div></div>
      <div class="info-bar__item">{ic("calendar")}<div><strong>Pré-agendamento simples</strong><span>Em poucos passos, direto para o WhatsApp</span></div></div>
    </div>
  </div>
</section>'''


# ------------------------------------------------------------------ HOME
def home(r):
    areas = "".join(f'''
      <a class="area-card" href="{r}especialidades/{s["slug"]}.html">
        <div class="area-card__top"><span class="area-card__ic">{ic(s["icon"])}</span><span class="area-card__num">0{i+1}</span></div>
        <div><h3 class="h3">{s["name"]}</h3><p>{s["short"]}</p>{link_arrow("Saiba mais", "", "span")}</div>
      </a>''' for i, s in enumerate(SPECS))

    journey = [
        ("Primeiro contato", "Você faz o pré-agendamento pelo site e escolhe o melhor formato: presencial, na Asa Sul, ou por telemedicina.", "oliveira", "50% 50%", "calendar", "Pré-agendamento enviado", "Presencial ou online · você escolhe"),
        ("Consulta de avaliação", "Cerca de 60 minutos com a Dra. Aclair para conhecer sua história, seus hábitos, seus exames e seus objetivos.", "dra_largo", "50% 22%", "clock", "Consulta · 60 minutos", "Escuta completa, sem pressa"),
        ("Plano personalizado", "Construímos juntos um plano de cuidado com metas realistas e prioridades claras.", "caderno", "50% 50%", "compass", "Seu plano de cuidado", "Prioridades definidas em conjunto"),
        ("Acompanhamento contínuo", "Retornos para ajustar o plano, revisar exames e acompanhar sua evolução, presencialmente ou online.", "tele", "50% 40%", "loop", "Próximo retorno agendado", "Ajustes conforme a sua evolução"),
        ("Autonomia ao longo da vida", "Hábitos consolidados e prevenção como rotina, para viver cada fase com mais saúde.", "caminhada", "50% 55%", "sun", "Cuidar hoje transforma o amanhã", "Prevenção como parte da rotina"),
    ]
    steps = "".join(f'<li><b>0{i+1}</b><span>{t[0]}</span></li>' for i, t in enumerate(journey))
    cards = "".join(f'''
      <article class="stack-card" style="--i:{i}">
        <div class="stack-card__bg">{pic(t[2], "", "(max-width: 920px) 100vw, 60vw", pos=t[3])}</div>
        <div class="stack-card__content">
          <span class="stack-card__num">Etapa 0{i+1}</span>
          <div class="chip"><span class="chip__ic">{ic(t[4])}</span><div><strong>{t[5]}</strong><small>{t[6]}</small></div></div>
          <div><h3>{t[0]}</h3><p>{t[1]}</p></div>
        </div>
      </article>''' for i, t in enumerate(journey))

    posts = "".join(post_card(p, r) for p in POSTS[:3])

    return f'''
<section class="hero">
  <div class="container hero__grid">
    <div class="hero__text">
      <p class="eyebrow fade-up" style="--d:0">{TITULO} · Brasília</p>
      <h1 class="display">
        <span class="line-reveal"><span style="--d:0">Cuidar hoje</span></span>
        <span class="line-reveal"><span style="--d:1"><em>transforma</em></span></span>
        <span class="line-reveal"><span style="--d:2">o amanhã.</span></span>
      </h1>
      <p class="lead fade-up" style="--d:3">Acompanhamento médico contínuo e personalizado para você viver com saúde, autonomia e qualidade de vida, hoje e nos próximos anos.</p>
      <div class="btn-row fade-up" style="--d:4">{agendar()}{btn("Conheça a Dra. Aclair", f"{r}sobre.html", "ghost")}</div>
      <ul class="hero__facts fade-up" style="--d:5">
        <li>{ic("pin")}Presencial na Asa Sul</li>
        <li>{ic("video")}Telemedicina</li>
        <li>{ic("clock")}Consultas de cerca de 60 min</li>
      </ul>
    </div>
    <div class="hero__media fade-up" style="--d:2">
      <img class="hero__dragonfly" src="{r}assets/img/libelula.png" alt="">
      <div class="arch">{pic("dra_retrato", "Dra. Aclair Dallagranna, Médica de Família e Comunidade", eager=True, pos="50% 18%")}</div>
      <div class="chip chip--a float"><span class="chip__ic"><img src="{r}assets/img/libelula-claro.png" alt=""></span><div><strong>{DRA}</strong><small>{TITULO}</small></div></div>
      <div class="chip chip--b float float--b"><span class="chip__dot"></span><div><strong>Médica desde 2010</strong><small>Cuidado contínuo e individualizado</small></div></div>
    </div>
  </div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee__track">
  {"".join('<div class="marquee__group">' + "".join(f"<span>{w}</span>{STAR}" for w in ["Prevenção", "Longevidade", "Autonomia", "Escuta", "Ciência", "Acompanhamento contínuo", "Qualidade de vida"]) + "</div>" for _ in range(2))}
</div></div>

<section class="section manifesto">
  <div class="container">
    <p class="eyebrow eyebrow--center" data-reveal>Nossa filosofia</p>
    <p class="manifesto__text" data-words>Uma medicina que cuida da pessoa, <em>não apenas da doença.</em> Escuta sem pressa, ciência como base e um plano feito para a <em>sua vida real.</em></p>
    <div class="manifesto__sign" data-reveal><img class="avatar" src="{r}assets/img/dra/dra-avatar.jpg" alt=""><span>{DRA} · {BRAND}</span></div>
  </div>
</section>

<section class="section" style="padding-top:0">
  <div class="container">
    <div class="sec-head">
      <div><p class="eyebrow" data-reveal>Áreas de atuação</p>
      <h2 class="title" data-reveal>Cuidado integral, <em>em cada fase</em> da vida.</h2></div>
      <div data-reveal><p class="lead" style="margin-bottom:22px">Seis frentes de cuidado que se complementam, sempre a partir de uma avaliação individualizada e de um acompanhamento contínuo.</p>{link_arrow("Ver todas as especialidades", f"{r}especialidades.html")}</div>
    </div>
    <div class="areas" data-stagger>{areas}</div>
  </div>
</section>

<section class="section section--sand texture">
  <div class="container about">
    <div class="about__media" data-reveal>
      <div class="about__img">{pic("dra_consultorio", "Dra. Aclair Dallagranna no consultório", pos="50% 20%")}</div>
      <div class="about__detail">{pic("eucalipto", "", "240px", widths=(500, 900))}</div>
    </div>
    <div>
      <p class="eyebrow" data-reveal>A médica</p>
      <h2 class="title" data-reveal>Dra. Aclair <em>Dallagranna</em></h2>
      <p class="lead" data-reveal style="margin-top:26px">Médica de Família e Comunidade desde 2010, com formação em envelhecimento saudável e em emagrecimento seguro e responsável.</p>
      <p data-reveal>Seu trabalho é acompanhar pessoas ao longo do tempo: entender a história de cada paciente, prevenir doenças, cuidar das condições crônicas e construir hábitos que façam sentido para a vida real.</p>
      <ul class="creds" data-stagger>
        <li>{ic("check")}Residência em Medicina de Família e Comunidade</li>
        <li>{ic("check")}Formação em envelhecimento saudável e em emagrecimento responsável</li>
        <li>{ic("check")}Referência técnica distrital no cuidado de doenças crônicas (SES-DF)</li>
        <li>{ic("check")}Atendimento presencial em Brasília e por telemedicina</li>
      </ul>
      <div class="btn-row" data-reveal>{btn("Conheça a trajetória", f"{r}sobre.html")}</div>
      <p class="reg" data-reveal style="margin-top:22px">{REG}</p>
    </div>
  </div>
</section>

{program_block(r)}

<section class="section">
  <div class="container journey">
    <div class="journey__aside">
      <p class="eyebrow" data-reveal>Jornada de saúde</p>
      <h2 class="title" data-reveal>Do primeiro contato <em>ao cuidado contínuo.</em></h2>
      <p class="lead" data-reveal style="margin-top:24px">Cada etapa foi pensada para que você tenha clareza, escuta e acompanhamento em todo o caminho.</p>
      <ol class="journey__steps">{steps}</ol>
      <div class="journey__progress"><i></i></div>
      <div class="btn-row" style="margin-top:36px" data-reveal>{btn("Como funciona", f"{r}como-funciona.html", "ghost")}</div>
    </div>
    <div class="stack">{cards}</div>
  </div>
</section>

{exp_block(r)}

<!-- VALIDAR: números do site atual (28.423+ atendimentos; 81+ médicos treinados — no Instagram consta "mais de 100"). -->
<section class="stats">
  <div class="floater f1" data-speed="-0.12">{pic("idosa_flores", "", "200px", widths=(500,))}</div>
  <div class="floater f2" data-speed="0.1">{pic("comida2", "", "160px", widths=(500,))}</div>
  <div class="floater f3" data-speed="-0.08">{pic("familia_dourada", "", "220px", widths=(500,))}</div>
  <div class="floater f4" data-speed="0.14">{pic("oliveira2", "", "200px", widths=(500,))}</div>
  <div class="floater f5" data-speed="-0.2">{pic("salvia", "", "120px", widths=(400,))}</div>
  <div class="stats__center">
    <p class="eyebrow eyebrow--center" data-reveal>Trajetória</p>
    <div class="stats__big" data-reveal><span data-count="28">0</span> mil<sup>+</sup></div>
    <p class="stats__label" data-reveal>atendimentos realizados ao longo da trajetória</p>
    <div class="stats__row" data-stagger>
      <div><strong><span data-count="15">0</span>+</strong><span>anos de medicina</span></div>
      <div><strong><span data-count="80">0</span>+</strong><span>médicos treinados</span></div>
      <div><strong>60 min</strong><span>de consulta, em média</span></div>
    </div>
  </div>
</section>

<section class="section section--sand texture">
  <div class="container">
    <div class="sec-head">
      <div><p class="eyebrow" data-reveal>Blog</p>
      <h2 class="title" data-reveal>Conteúdo para <em>cuidar melhor</em> de você.</h2></div>
      <div data-reveal><p class="lead" style="margin-bottom:22px">Informação confiável sobre prevenção, longevidade e qualidade de vida, em linguagem clara.</p>{link_arrow("Ver todos os artigos", f"{r}blog.html")}</div>
    </div>
    <div class="posts" data-stagger>{posts}</div>
  </div>
</section>

<section class="section">
  <div class="container faq-wrap">
    <div class="faq-wrap__aside">
      <p class="eyebrow" data-reveal>Dúvidas frequentes</p>
      <h2 class="title" data-reveal>Antes da <em>primeira consulta.</em></h2>
      <p class="lead" data-reveal style="margin:24px 0 34px">Reunimos as perguntas mais comuns sobre consultas, telemedicina e agendamento.</p>
      <div data-reveal>{btn("Ver todas as dúvidas", f"{r}faq.html", "ghost")}</div>
    </div>
    <div data-reveal>{faq_html(FAQ_HOME)}</div>
  </div>
</section>

{cta_block(r)}
'''


# ------------------------------------------------------------------ SOBRE
def sobre(r):
    return f'''
<section class="page-hero">
  <div class="container page-hero__grid" style="align-items:center">
    <div>
      <nav class="crumbs fade-up"><a href="{r}index.html">Início</a><span>/</span>A médica</nav>
      <p class="eyebrow fade-up" style="--d:0">A médica</p>
      <h1 class="display"><span class="line-reveal"><span>Dra. Aclair</span></span><span class="line-reveal"><span style="--d:1"><em>Dallagranna</em></span></span></h1>
      <p class="lead fade-up" style="--d:2">Médica de Família e Comunidade desde 2010, com formação em envelhecimento saudável e em emagrecimento seguro e responsável. Atende em Brasília e por telemedicina.</p>
      <div class="btn-row fade-up" style="--d:3;margin-top:36px">{agendar()}</div>
      <p class="reg fade-up" style="--d:4;margin-top:22px">{REG}</p>
    </div>
    <div class="hero__media fade-up" style="--d:2;justify-self:end">
      <div class="arch">{pic("dra_consultorio", "Dra. Aclair Dallagranna no consultório", eager=True, pos="50% 15%")}</div>
    </div>
  </div>
</section>

<section class="section section--paper">
  <div class="container split">
    <div>
      <p class="eyebrow" data-reveal>Trajetória</p>
      <h2 class="title" data-reveal>Uma trajetória dedicada ao <em>cuidado integral.</em></h2>
    </div>
    <div class="prose" data-reveal>
      <!-- VALIDAR: texto baseado no site atual e na apresentação do Instagram. -->
      <p>Médica desde 2010, a Dra. Aclair fez residência em Medicina de Família e Comunidade e dedicou a carreira ao cuidado contínuo das pessoas, em diferentes fases da vida.</p>
      <p>Atuou como Referência Técnica Distrital pela Secretaria de Saúde do Distrito Federal, com ênfase no cuidado de doenças crônicas, e se dedica à formação de novos médicos, incluindo treinamentos para a inserção de DIU.</p>
      <p>Hoje, seu trabalho une Medicina do Estilo de Vida, longevidade, emagrecimento responsável e saúde da mulher, com uma convicção: viver mais é consequência, e viver bem é uma escolha que começa com pequenas ações.</p>
      <p>A {BRAND} nasce desse propósito: oferecer gestão personalizada da saúde, com tempo para escutar, ciência para orientar e continuidade para acompanhar.</p>
    </div>
  </div>
  <div class="container">
    <div class="stats__row" style="margin-top:90px" data-stagger>
      <div><strong><span data-count="28">0</span> mil+</strong><span>atendimentos realizados</span></div>
      <div><strong><span data-count="400">0</span>+</strong><span>DIUs inseridos</span></div>
      <div><strong><span data-count="80">0</span>+</strong><span>médicos treinados</span></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split">
    <div class="about__media" data-reveal>
      <div class="about__img">{pic("dra_retrato", "Dra. Aclair Dallagranna com jaleco da Medicina de Família", pos="50% 25%")}</div>
    </div>
    <div>
      <p class="eyebrow" data-reveal>Formação</p>
      <h2 class="title title--md" data-reveal>Ciência como base, <em>escuta como método.</em></h2>
      <!-- VALIDAR: instituições de graduação/residência e a especialidade de cada RQE. Informações do Instagram. -->
      <ol class="timeline" style="margin-top:44px" data-stagger>
        <li><b>2010</b><strong>Graduação em Medicina</strong><span>Instituição a confirmar</span></li>
        <li><b>2014</b><strong>Residência em Medicina de Família e Comunidade</strong><span>Especialista com Registro de Qualificação (RQE)</span></li>
        <li><b>Pós-graduação</b><strong>Ensino médico</strong><span>Formação de mais de 80 novos médicos ao longo da trajetória</span></li>
        <li><b>2021</b><strong>Pós-graduação em Acupuntura médica</strong><span>CMBA</span></li>
        <li><b>Formação complementar</b><strong>Envelhecimento saudável e emagrecimento seguro e responsável</strong><span>Medicina do Estilo de Vida e longevidade</span></li>
        <li><b>Formação complementar</b><strong>Terapia Comunitária Integrativa</strong><span>Cuidado em grupo e escuta comunitária</span></li>
      </ol>
    </div>
  </div>
</section>

<section class="section section--olive texture">
  <div class="container">
    <div class="sec-head">
      <div><p class="eyebrow" data-reveal>Filosofia de atendimento</p>
      <h2 class="title" data-reveal>O que guia <em>cada consulta.</em></h2></div>
      <p class="lead" data-reveal style="color:rgba(232,223,209,.85)">Quatro princípios que orientam a forma de cuidar da {BRAND}.</p>
    </div>
    <div class="values" data-stagger>
      <div class="value"><b>i.</b><h3>Escuta</h3><p>Tempo para entender sua história, sem pressa e sem julgamentos.</p></div>
      <div class="value"><b>ii.</b><h3>Ciência</h3><p>Decisões baseadas em evidências e explicadas com clareza.</p></div>
      <div class="value"><b>iii.</b><h3>Prevenção</h3><p>Cuidar antes, para viver melhor depois.</p></div>
      <div class="value"><b>iv.</b><h3>Autonomia</h3><p>Preservar a independência e a capacidade de decidir sobre a própria vida.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container split split--center">
    <div>
      <p class="eyebrow" data-reveal>Abordagem médica</p>
      <h2 class="title title--md" data-reveal>Cuidado integral, <em>do jeito certo para você.</em></h2>
      <ul class="check-list" style="margin-top:40px" data-stagger>
        <li>{ic("check")}<div><strong>Olhar para a pessoa inteira</strong><span>Saúde física, emocional, rotina e contexto familiar.</span></div></li>
        <li>{ic("check")}<div><strong>Plano individualizado</strong><span>Nada de protocolos genéricos: prioridades definidas para o seu momento.</span></div></li>
        <li>{ic("check")}<div><strong>Decisão compartilhada</strong><span>Você entende as opções e participa das escolhas.</span></div></li>
        <li>{ic("check")}<div><strong>Acompanhamento contínuo</strong><span>Um cuidado que segue com você ao longo dos anos.</span></div></li>
      </ul>
    </div>
    <div class="about__media" data-reveal>
      <div class="about__img">{pic("familia2", "Família reunida ao ar livre (foto ilustrativa)", "(max-width: 920px) 90vw, 45vw", pos="50% 40%")}</div>
      <div class="about__detail">{pic("oliveira", "", "240px", widths=(500, 900))}</div>
    </div>
  </div>
</section>

<section class="section section--sand texture" style="text-align:center">
  <div class="container">
    <img class="avatar avatar--lg" src="{r}assets/img/dra/dra-avatar.jpg" alt="{DRA}" data-reveal>
    <p class="title" data-reveal style="max-width:16em;margin:0 auto">“Toda grande transformação começa com <em>uma pequena decisão.</em>”</p>
    <p class="reg" style="margin-top:30px" data-reveal>{DRA}</p>
  </div>
</section>

{cta_block(r)}
'''


# ------------------------------------------------------------------ ESPECIALIDADES (hub)
def especialidades(r):
    rows = "".join(f'''
    <article class="spec-row">
      <a class="spec-row__img" href="{r}especialidades/{s["slug"]}.html" data-reveal="clip">{pic(s["img"], s["name"], "(max-width: 920px) 100vw, 50vw", pos=s["pos"])}</a>
      <div>
        <span class="num" data-reveal>0{i+1}</span>
        <h2 class="title title--md" data-reveal>{s["name"]}</h2>
        <p class="lead" data-reveal>{s["intro"]}</p>
        <ul data-stagger>{"".join(f"<li>{t}</li>" for t in s["tags"])}</ul>
        <div class="btn-row" data-reveal>{btn("Conhecer", f"{r}especialidades/{s['slug']}.html", "ghost")}{agendar(label="Agendar", area=s["name"])}</div>
      </div>
    </article>''' for i, s in enumerate(SPECS))
    return f'''
<section class="page-hero page-hero--center">
  <div class="container">
    <nav class="crumbs fade-up" style="justify-content:center"><a href="{r}index.html">Início</a><span>/</span>Especialidades</nav>
    <p class="eyebrow eyebrow--center fade-up">Áreas de atuação</p>
    <h1 class="display"><span class="line-reveal"><span>Cuidado integral,</span></span><span class="line-reveal"><span style="--d:1"><em>em cada fase.</em></span></span></h1>
    <p class="lead fade-up" style="--d:2">Seis áreas que se complementam e partem do mesmo princípio: avaliação individualizada, prevenção e acompanhamento contínuo.</p>
  </div>
</section>
<section class="section" style="padding-top:20px">
  <div class="container spec-rows">{rows}</div>
</section>
{cta_block(r)}
'''


# ------------------------------------------------------------------ ESPECIALIDADE (página interna)
def spec_page(s):
    def body(r):
        i = SPECS.index(s)
        para = ""
        if s.get("para"):
            items = "".join(f'<li>{ic("check")}<div><strong>{a}</strong><span>{b}</span></div></li>' for a, b in s["para"])
            para = f'''
<section class="section section--paper">
  <div class="container split">
    <div>
      <p class="eyebrow" data-reveal>Para quem é</p>
      <h2 class="title title--md" data-reveal>Um cuidado pensado <em>para você.</em></h2>
    </div>
    <ul class="check-list" data-stagger>{items}</ul>
  </div>
</section>'''
        pil = ""
        if s.get("pilares"):
            cards = "".join(f'<div class="pillar"><div class="pillar__ic">{ic(a)}</div><h3 class="h3">{b}</h3><p>{c}</p></div>' for a, b, c in s["pilares"])
            pil = f'''
<section class="section">
  <div class="container">
    <div class="sec-head">
      <div><p class="eyebrow" data-reveal>O que cuidamos</p>
      <h2 class="title title--md" data-reveal>Frentes de <em>cuidado.</em></h2></div>
      <p class="lead" data-reveal>Cada frente é avaliada de forma individual e entra no plano de acordo com as suas prioridades.</p>
    </div>
    <div class="pillars" data-stagger>{cards}</div>
  </div>
</section>'''
        como = "".join(f'<div class="exp__item"><div class="exp__ic exp__ic--num">0{k+1}</div><h3 class="h3">{a}</h3><p>{b}</p></div>' for k, (a, b) in enumerate(s["como"]))
        notice = f'<div class="notice" style="margin-top:48px" data-reveal>{ic("info")}<span>{s["notice"]}</span></div>' if s.get("notice") else ""
        others = [o for o in SPECS if o is not s][:3] if i < 3 else [o for o in SPECS if o is not s][-3:]
        rel = "".join(f'<a href="{r}especialidades/{o["slug"]}.html">{o["name"]}{ic("arrow")}</a>' for o in others)
        return f'''
<section class="page-hero">
  <div class="container page-hero__grid">
    <div>
      <nav class="crumbs fade-up"><a href="{r}index.html">Início</a><span>/</span><a href="{r}especialidades.html">Especialidades</a><span>/</span>{s["name"]}</nav>
      <p class="eyebrow fade-up">{s["name"]}</p>
      <h1 class="title" style="font-size:clamp(2.6rem,5.2vw,5rem)"><span class="line-reveal"><span>{s["title"]}</span></span></h1>
      <p class="lead fade-up" style="--d:2">{s["intro"]}</p>
      <div class="btn-row fade-up" style="--d:3;margin-top:36px">{agendar(area=s["name"])}{btn("Como funciona", f"{r}como-funciona.html", "ghost")}</div>
    </div>
    <div class="page-hero__img fade-up" style="--d:2">{pic(s["img"], s["name"] + " (foto ilustrativa)", "(max-width: 920px) 100vw, 45vw", eager=True, pos=s["pos"])}</div>
  </div>
</section>
{para}
{pil}
<section class="section section--mist texture">
  <div class="container">
    <div class="sec-head">
      <div><p class="eyebrow" data-reveal>Como cuidamos</p>
      <h2 class="title title--md" data-reveal>Passo a passo, <em>com você.</em></h2></div>
      <p class="lead" data-reveal>Uma abordagem individualizada, baseada em evidências e sem promessas de resultado: cada pessoa tem o seu caminho.</p>
    </div>
    <div class="exp" data-stagger>{como}</div>
    {notice}
  </div>
</section>
<section class="section doc-quote">
  <div class="container">
    <div class="doc-quote__in" data-reveal>
      <img src="{r}assets/img/dra/dra-avatar.jpg" alt="{DRA}">
      <div>
        <p class="title title--md"><em>“{s["quote"]}”</em></p>
        <p class="reg" style="margin-top:18px">{DRA} · {TITULO}</p>
      </div>
    </div>
  </div>
</section>
<section class="section section--sand texture">
  <div class="container faq-wrap">
    <div class="faq-wrap__aside">
      <p class="eyebrow" data-reveal>Dúvidas</p>
      <h2 class="title title--md" data-reveal>Perguntas <em>frequentes.</em></h2>
      <div data-reveal style="margin-top:30px">{link_arrow("Ver todas as dúvidas", f"{r}faq.html")}</div>
    </div>
    <div data-reveal>{faq_html(s["faq"])}</div>
  </div>
</section>
<section class="section" style="padding-bottom:0">
  <div class="container">
    <p class="eyebrow" data-reveal>Outras áreas de atuação</p>
    <div class="related" data-stagger>{rel}</div>
    <div class="notice" style="margin-top:28px">{ic("info")}<span>Conteúdo informativo. Não substitui a avaliação médica individual.</span></div>
  </div>
</section>
{cta_block(r)}
'''
    return body


# ------------------------------------------------------------------ COMO FUNCIONA
def como_funciona(r):
    steps = [
        ("Primeiro contato", "Você faz o pré-agendamento pelo site, conta o que procura e escolhe o formato: presencial, na Asa Sul, ou por telemedicina.", "oliveira", "50% 50%", "calendar", "Pré-agendamento enviado"),
        ("Consulta de avaliação", "Cerca de 60 minutos com a Dra. Aclair para conhecer sua história, seus hábitos, seus exames e seus objetivos.", "dra_largo", "50% 20%", "clock", "Consulta com a Dra. Aclair"),
        ("Plano personalizado", "Construímos juntos um plano de cuidado com metas realistas, prioridades claras e orientações práticas.", "caderno", "50% 50%", "compass", "Plano de cuidado definido"),
        ("Acompanhamento contínuo", "Retornos para revisar exames, ajustar o plano e acompanhar sua evolução, presencialmente ou online.", "tele", "50% 40%", "loop", "Próximo retorno agendado"),
        ("Autonomia ao longo da vida", "Hábitos consolidados e prevenção como rotina, para viver cada fase com mais saúde e independência.", "casal_abraco", "50% 45%", "sun", "Cuidar hoje transforma o amanhã"),
    ]
    tabs = "".join(f'<button class="stepper__tab{" is-active" if i == 0 else ""}" role="tab" aria-selected="{"true" if i == 0 else "false"}"><b>0{i+1}</b><div><strong>{t[0]}</strong><span>{t[1]}</span></div></button>' for i, t in enumerate(steps))
    figs = "".join(f'<figure class="{"is-active" if i == 0 else ""}">{pic(t[2], t[0], "(max-width: 920px) 100vw, 50vw", pos=t[3])}<div class="chip"><span class="chip__ic">{ic(t[4])}</span><div><strong>{t[5]}</strong><small>Etapa 0{i+1} de 05</small></div></div></figure>' for i, t in enumerate(steps))
    return f'''
<section class="page-hero page-hero--center">
  <div class="container">
    <nav class="crumbs fade-up" style="justify-content:center"><a href="{r}index.html">Início</a><span>/</span>Como funciona</nav>
    <p class="eyebrow eyebrow--center fade-up">Experiência do paciente</p>
    <h1 class="display"><span class="line-reveal"><span>Como funciona</span></span><span class="line-reveal"><span style="--d:1"><em>o seu cuidado.</em></span></span></h1>
    <p class="lead fade-up" style="--d:2">Do pré-agendamento ao acompanhamento contínuo, cada etapa foi pensada para que você tenha tempo, clareza e um plano feito para a sua vida.</p>
  </div>
</section>

<section class="section" style="padding-top:10px">
  <div class="container">
    <p class="eyebrow" data-reveal>Jornada de saúde</p>
    <div class="stepper">
      <div class="stepper__tabs" role="tablist" data-reveal>{tabs}</div>
      <div class="stepper__stage" data-reveal="clip">{figs}</div>
    </div>
  </div>
</section>

{exp_block(r)}

<section class="section">
  <div class="container split split--center">
    <div class="about__media" data-reveal>
      <div class="about__img">{pic("tele", "Paciente em consulta por telemedicina (foto ilustrativa)", "(max-width: 920px) 90vw, 45vw", pos="45% 40%")}</div>
    </div>
    <div>
      <p class="eyebrow" data-reveal>Telemedicina</p>
      <h2 class="title title--md" data-reveal>O mesmo cuidado, <em>onde você estiver.</em></h2>
      <p class="lead" data-reveal style="margin:24px 0 10px">A consulta online segue a mesma lógica da presencial: tempo, escuta e um plano individualizado.</p>
      <ul class="check-list" style="margin-top:30px" data-stagger>
        <li>{ic("calendar")}<div><strong>Faça o pré-agendamento</strong><span>Conte o que procura e escolha a telemedicina como formato.</span></div></li>
        <li>{ic("video")}<div><strong>Receba o link</strong><span>No dia e horário marcados, você recebe o link da videoconferência.</span></div></li>
        <li>{ic("receipt")}<div><strong>Tenha seus exames em mãos</strong><span>E a lista de medicamentos e suplementos em uso.</span></div></li>
        <li>{ic("leaf")}<div><strong>Escolha um lugar tranquilo</strong><span>Com boa conexão e privacidade para conversar.</span></div></li>
      </ul>
      <div class="btn-row" style="margin-top:34px" data-reveal>{agendar(label="Agendar teleconsulta")}</div>
    </div>
  </div>
</section>

{program_block(r)}

<section class="section">
  <div class="container faq-wrap">
    <div class="faq-wrap__aside">
      <p class="eyebrow" data-reveal>Dúvidas</p>
      <h2 class="title title--md" data-reveal>Sobre consultas e <em>agendamento.</em></h2>
      <div data-reveal style="margin-top:30px">{link_arrow("Ver todas as dúvidas", f"{r}faq.html")}</div>
    </div>
    <div data-reveal>{faq_html(["primeira", "duracao", "exames", "convenio", "vida"])}</div>
  </div>
</section>

{cta_block(r)}
'''


# ------------------------------------------------------------------ BLOG
def blog(r):
    f = POSTS[0]
    cats = [("todos", "Todos")] + [(c, n) for c, n in dict((p["cat"], p["catname"]) for p in POSTS).items()]
    filt = "".join(f'<button class="filter{" is-active" if c == "todos" else ""}" data-filter="{c}">{n}</button>' for c, n in cats)
    posts = "".join(post_card(p, r) for p in POSTS[1:])
    return f'''
<section class="page-hero page-hero--center">
  <div class="container">
    <nav class="crumbs fade-up" style="justify-content:center"><a href="{r}index.html">Início</a><span>/</span>Blog</nav>
    <p class="eyebrow eyebrow--center fade-up">Blog</p>
    <h1 class="display"><span class="line-reveal"><span>Conteúdo para</span></span><span class="line-reveal"><span style="--d:1"><em>viver melhor.</em></span></span></h1>
    <p class="lead fade-up" style="--d:2">Prevenção, longevidade, hábitos e qualidade de vida, com base em evidências e em linguagem clara.</p>
  </div>
</section>
<section class="section" style="padding-top:10px">
  <div class="container">
    <a class="featured" href="{r}blog/{f["slug"]}.html" data-reveal>
      <div class="featured__img">{pic(f["img"], f["title"], "(max-width: 920px) 100vw, 60vw", pos=f["pos"])}</div>
      <div>
        <div class="post-card__meta"><span class="tag">Destaque</span><span>{f["catname"]} · {f["min"]} min de leitura</span></div>
        <h2 class="title title--md">{f["title"]}</h2>
        <p class="lead" style="margin:20px 0 28px">{f["excerpt"]}</p>
        {link_arrow("Ler artigo", "", "span")}
      </div>
    </a>
    <div class="filters" data-reveal>{filt}</div>
    <div class="posts" data-stagger>{posts}</div>
  </div>
</section>
{cta_block(r, "Quer conversar sobre <em>a sua saúde?</em>")}
'''


def artigo(r):
    p = POSTS[0]
    rel = "".join(post_card(x, r) for x in POSTS[1:4])
    toc = [("envelhecer-bem", "O que é envelhecer bem"), ("habitos", "Cinco hábitos que fazem diferença"),
           ("acompanhamento", "Por que o acompanhamento ajuda"), ("comecar", "Por onde começar")]
    toc_html = "".join(f'<a href="#{a}">{b}</a>' for a, b in toc)
    return f'''
<div class="read-progress" aria-hidden="true"></div>
<section class="article-hero">
  <div class="container">
    <nav class="crumbs fade-up" style="justify-content:center"><a href="{r}index.html">Início</a><span>/</span><a href="{r}blog.html">Blog</a><span>/</span>{p["catname"]}</nav>
    <span class="tag fade-up">{p["catname"]}</span>
    <h1 class="title" style="margin-top:24px"><span class="line-reveal"><span>{p["title"]}</span></span></h1>
    <div class="article-meta fade-up" style="--d:2"><img class="avatar avatar--sm" src="{r}assets/img/dra/dra-avatar.jpg" alt=""><span>Por {DRA}</span><span>·</span><span>{p["min"]} min de leitura</span></div>
  </div>
</section>
<div class="container"><div class="wide-img" data-reveal="clip">{pic(p["img"], p["title"], "100vw", eager=True, pos=p["pos"])}</div></div>
<section class="section" style="padding-top:80px">
  <div class="container article-layout">
    <nav class="toc" aria-label="Neste artigo"><b>Neste artigo</b>{toc_html}</nav>
    <article class="article-body">
      <!-- VALIDAR: artigo de exemplo — revisão técnica da Dra. antes de publicar. -->
      <div class="prose">
        <p class="lead">Quando se fala em longevidade, é comum pensar apenas em viver mais. Mas a pergunta mais importante talvez seja outra: <em>como</em> queremos viver esses anos?</p>
        <p>Longevidade com qualidade significa manter autonomia, disposição, memória e independência pelo maior tempo possível. E boa parte disso se constrói com escolhas feitas hoje, muito antes de qualquer problema aparecer.</p>
        <h2 id="envelhecer-bem">O que é envelhecer bem</h2>
        <p>Envelhecer bem não é evitar a passagem do tempo, e sim preservar a capacidade de fazer o que é importante para você: caminhar, trabalhar, conviver, viajar, cuidar de si e de quem ama. Essa capacidade depende da saúde física, mas também do sono, das relações, da saúde emocional e do acesso a um cuidado médico contínuo.</p>
        <h2 id="habitos">Cinco hábitos que fazem diferença</h2>
        <h3>1. Movimente-se, e inclua força</h3>
        <p>A atividade física regular está entre as medidas mais consistentes para a saúde ao longo da vida. Além dos exercícios aeróbicos, os exercícios de força ajudam a preservar a massa muscular e o equilíbrio, que são importantes para a autonomia e a prevenção de quedas.</p>
        <h3>2. Durma bem</h3>
        <p>O sono influencia o humor, a memória, o apetite e o metabolismo. Para a maioria dos adultos, recomenda-se ao menos sete horas por noite, com horários regulares.</p>
        <h3>3. Coma comida de verdade</h3>
        <p>O Guia Alimentar para a População Brasileira recomenda que a alimentação tenha como base alimentos in natura ou minimamente processados, com moderação nos ultraprocessados. Mais do que regras rígidas, vale construir uma rotina possível e prazerosa.</p>
        <h3>4. Cultive vínculos</h3>
        <p>Relações próximas, convivência e propósito também fazem parte da saúde. O isolamento social está associado a pior saúde física e mental ao longo dos anos.</p>
        <h3>5. Faça prevenção no tempo certo</h3>
        <p>Rastreamentos, vacinas e o controle de pressão, glicemia e colesterol devem seguir a sua idade, o seu histórico e os seus fatores de risco. Mais exames não significam, necessariamente, mais saúde.</p>
        <blockquote>Viver mais é consequência. Viver bem é escolha, e começa com pequenas ações.</blockquote>
        <h2 id="acompanhamento">Por que o acompanhamento ajuda</h2>
        <p>Cada pessoa tem uma história, um contexto e prioridades diferentes. O acompanhamento médico contínuo permite identificar o que mais importa no seu caso, definir metas realistas e ajustar o plano ao longo do tempo, em vez de depender de consultas isoladas.</p>
        <h2 id="comecar">Por onde começar</h2>
        <ul>
          <li>Escolha <strong>uma</strong> mudança possível para as próximas semanas.</li>
          <li>Organize seus exames e a lista de medicamentos em uso.</li>
          <li>Converse com um médico de referência sobre a sua prevenção.</li>
        </ul>
        <div class="notice" style="margin-top:40px">{ic("info")}<span>Este conteúdo é informativo e não substitui a consulta médica. Cada caso deve ser avaliado individualmente.</span></div>
      </div>
    </article>
    <aside><div class="author"><img src="{r}assets/img/dra/dra-avatar.jpg" alt="{DRA}"><div><strong>{DRA}</strong><span>{TITULO}<br>{REG}</span></div></div></aside>
  </div>
</section>
<section class="section section--sand texture">
  <div class="container">
    <div class="sec-head"><div><p class="eyebrow">Continue lendo</p><h2 class="title title--md">Outros <em>artigos.</em></h2></div></div>
    <div class="posts" data-stagger>{rel}</div>
  </div>
</section>
{cta_block(r)}
'''


# ------------------------------------------------------------------ FAQ
def faq_page(r):
    groups = "".join(f'<div class="faq-group" data-reveal><h3 class="h3">{g}</h3>{faq_html(keys)}</div>' for g, keys in FAQ_GROUPS)
    return f'''
<section class="page-hero page-hero--center">
  <div class="container">
    <nav class="crumbs fade-up" style="justify-content:center"><a href="{r}index.html">Início</a><span>/</span>Dúvidas</nav>
    <p class="eyebrow eyebrow--center fade-up">Perguntas frequentes</p>
    <h1 class="display"><span class="line-reveal"><span>Tire suas</span></span><span class="line-reveal"><span style="--d:1"><em>dúvidas.</em></span></span></h1>
    <p class="lead fade-up" style="--d:2">Consultas, telemedicina, agendamento e programas. Se a sua pergunta não estiver aqui, conte no pré-agendamento.</p>
  </div>
</section>
<section class="section" style="padding-top:20px">
  <div class="container faq-wrap">
    <div class="faq-wrap__aside">
      <div class="contact-card contact-card--stack" data-reveal>
        <img class="avatar" src="{r}assets/img/dra/dra-avatar.jpg" alt="{DRA}">
        <div><strong>Ainda com dúvidas?</strong><span>Faça o pré-agendamento e conte o que você procura. A equipe retorna pelo WhatsApp.</span></div>
        <div class="btn-row">{agendar(label="Fazer pré-agendamento")}</div>
      </div>
    </div>
    <div>{groups}</div>
  </div>
</section>
{cta_block(r)}
'''


# ------------------------------------------------------------------ CONTATO
def contato(r):
    return f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs fade-up"><a href="{r}index.html">Início</a><span>/</span>Contato</nav>
    <p class="eyebrow fade-up">Agendamento e contato</p>
    <h1 class="display"><span class="line-reveal"><span>Vamos</span></span><span class="line-reveal"><span style="--d:1"><em>conversar?</em></span></span></h1>
    <p class="lead fade-up" style="--d:2">Faça o pré-agendamento abaixo: em poucos passos você conta o que procura, e a mensagem chega pronta no WhatsApp da equipe, que retorna para confirmar dia, horário e formato.</p>
  </div>
</section>
<section class="section" style="padding-top:10px">
  <div class="container">
    <div data-reveal>{booking(r, "p", inline=True)}</div>
  </div>
</section>
<section class="section" style="padding-top:0">
  <div class="container contact-info">
    <div class="contact-cards" data-stagger>
      <div class="contact-card"><span class="ic">{WA_SVG}</span><div><strong>WhatsApp</strong><span>{WA_TXT}</span></div></div>
      <div class="contact-card"><span class="ic">{ic("pin")}</span><div><strong>Consultório</strong><span>{ADDRESS_1}<br>{ADDRESS_2}</span><br><a class="link-arrow" href="{MAPS_DIR}" target="_blank" rel="noopener">Como chegar{ic("arrow")}</a></div></div>
      <!-- VALIDAR: horário de atendimento não informado. -->
      <div class="contact-card"><span class="ic">{ic("clock")}</span><div><strong>Atendimento</strong><span>Com hora marcada, presencial ou por telemedicina. Horários a confirmar.</span></div></div>
      <div class="contact-card"><span class="ic">{ic("insta")}</span><div><strong>Instagram</strong><span>{INSTA_HANDLE}</span><br><a class="link-arrow" href="{INSTAGRAM}" target="_blank" rel="noopener">Seguir{ic("arrow")}</a></div></div>
    </div>
    <div class="map" data-reveal><iframe src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa: {ADDRESS_1}, Brasília"></iframe></div>
  </div>
</section>
'''


# ------------------------------------------------------------------ build
JSONLD = {
    "@context": "https://schema.org",
    "@type": "MedicalClinic",
    "name": "Atthis — Gestão personalizada da saúde",
    "slogan": "Cuidar hoje transforma o amanhã",
    "telephone": "+55 61 99283-1370",
    "address": {"@type": "PostalAddress", "streetAddress": "SEPS 712/912, Ed. Via Brasil, Sala 313", "addressLocality": "Brasília",
                "addressRegion": "DF", "postalCode": "70360-510", "addressCountry": "BR"},
    "medicalSpecialty": ["PrimaryCare", "PreventiveMedicine"],
    "employee": {"@type": "Physician", "name": "Dra. Aclair Dallagranna", "description": "Médica de Família e Comunidade · CRM-DF 18142 · RQE 15614 · RQE 20140"},
    "sameAs": [INSTAGRAM],
}

if __name__ == "__main__":
    page("index.html", "Início", "Medicina de Família e Comunidade em Brasília: cuidado contínuo, preventivo e individualizado com a Dra. Aclair Dallagranna. Presencial na Asa Sul ou por telemedicina.", home, "index.html", JSONLD)
    page("sobre.html", "A médica", "Conheça a Dra. Aclair Dallagranna, Médica de Família e Comunidade desde 2010, com formação em envelhecimento saudável e emagrecimento seguro e responsável.", sobre, "sobre.html")
    page("especialidades.html", "Especialidades", "Medicina de Família, Estilo de Vida, Longevidade, Emagrecimento Saudável, Saúde da Mulher e Medicina Preventiva em Brasília.", especialidades, "especialidades.html")
    for s in SPECS:
        page(f"especialidades/{s['slug']}.html", s["name"], s["short"], spec_page(s), "especialidades.html")
    page("como-funciona.html", "Como funciona", "Do pré-agendamento ao acompanhamento contínuo: como funciona a consulta e a jornada de saúde na Atthis.", como_funciona, "como-funciona.html")
    page("blog.html", "Blog", "Conteúdos sobre prevenção, longevidade, hábitos e qualidade de vida.", blog, "blog.html")
    page(f"blog/{POSTS[0]['slug']}.html", POSTS[0]["title"], POSTS[0]["excerpt"], artigo, "blog.html")
    page("faq.html", "Dúvidas frequentes", "Perguntas frequentes sobre consultas, telemedicina, agendamento e reembolso.", faq_page, "faq.html")
    page("contato.html", "Contato e agendamento", "Faça o pré-agendamento da sua consulta com a Dra. Aclair Dallagranna. Consultório na Asa Sul, Brasília-DF, e telemedicina.", contato, "contato.html")
