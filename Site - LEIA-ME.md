# Site Atthis — Dra. Aclair Dallagranna (layout para apresentação)

## Link para a cliente
https://guleite.github.io/atthis-medicina-site/ (GitHub Pages, atualiza sozinho a cada envio ao repositório `guleite/atthis-medicina-site`).
As páginas estão marcadas como `noindex` (não aparecem no Google) enquanto o conteúdo está em validação. Quando o site for ao ar de verdade, remover a linha `<meta name="robots" ...>` em `site-fonte/build.py` e regenerar.

## Como abrir
- Rápido: abra `site/index.html` no navegador (precisa de internet para fontes e fotos do banco de imagens).
- Com servidor local (recomendado): na pasta do projeto, rode `python -m http.server 5510 -d site` e acesse http://localhost:5510

## Estrutura
- `site/` — o site pronto (HTML estático). Pode ser enviado assim para qualquer hospedagem.
  - `assets/css/style.css` — visual. Cores e fontes nas variáveis do topo (`:root`).
  - `assets/js/main.js` — animações, interações e o pré-agendamento (sem bibliotecas externas).
  - `assets/img/` — logo completo em SVG (colorido e claro), libélula, favicon.
  - `assets/img/dra/` — fotos REAIS da Dra. (da LP antiga), recortadas e tratadas localmente.
- `site-fonte/build.py` — **todo o conteúdo do site** (textos, FAQ, especialidades, blog, fotos, perguntas do pré-agendamento).
  Para editar: altere este arquivo e rode `python site-fonte/build.py` (regera todas as páginas).
- `site-fonte/vetorizar_logo.py` — gera o logo em SVG a partir da imagem enviada pelo cliente.
- `fotos-dra/lp/` — fotos originais da Dra. baixadas da LP antiga.

## Páginas (14)
Início · A médica · Especialidades (+ 6 páginas internas) · Como funciona · Blog · Artigo de exemplo · Dúvidas · Contato/Pré-agendamento.

## Pré-agendamento (pop-up)
Todos os botões "Agendar" (cabeçalho, seções, botão flutuante) abrem um pop-up em 6 etapas:
1. Nome, WhatsApp (com máscara), e-mail opcional e para quem é a consulta.
2. Áreas de interesse (cartões, múltipla escolha; já vem marcada a área da página de onde a pessoa veio).
3. Objetivos (múltipla escolha + campo livre).
4. Faixa etária, acompanhamento médico atual e condições já diagnosticadas (opcional).
5. Formato (presencial/telemedicina), melhor período, como conheceu e mensagem.
6. Revisão com resumo, prévia da mensagem do WhatsApp e consentimento (LGPD).
Ao enviar, abre o WhatsApp (61) 99283-1370 com a mensagem pronta e organizada. Na página de Contato, o mesmo formulário aparece embutido.
Para mudar perguntas/opções: listas `BK_...` no `build.py`.

## Interações
- Cartões das áreas com brilho que segue o cursor; jornada de saúde em cartões empilhados na rolagem.
- Manifesto que "acende" palavra a palavra; contadores; fotos flutuantes com parallax.
- Jornada por abas (Como funciona); filtro do blog; botões lado a lado/empilhados sempre com a mesma largura.
- Menu mobile em tela cheia; respeita "reduzir movimento".

## ⚠️ Antes de publicar — validar com a cliente
1. **Fotos da Dra.**: há só 2 fotos profissionais (LP antiga). Para a versão final, pedir mais fotos (consultório, atendimento).
2. **Demais fotos**: banco gratuito (Unsplash), carregadas por link. Ilustrativas.
3. **Trajetória** (página A médica, tirada do Instagram): datas, instituições e especialidade de cada RQE.
4. **Números**: 28 mil+ atendimentos, 400+ DIUs, 80+ médicos treinados (site diz 81+, Instagram diz 100+), 15+ anos.
5. **Programa Vida Atthis**: o texto das etapas é genérico. Falta receber o que o programa inclui.
6. **Horário de atendimento** e e-mail (não informados).
7. **Blog**: o artigo de exemplo precisa da revisão técnica da Dra. Os demais cards apontam para esse mesmo artigo (modelo).
8. Todo conteúdo médico deve ser validado pela Dra. antes de ir ao ar (Resolução CFM nº 2.336/2023).
9. **Logo**: o SVG foi vetorizado a partir de uma imagem. Se o cliente tiver o arquivo vetorial original, substituir.

No HTML, os trechos pendentes estão marcados com comentários `<!-- VALIDAR: ... -->`.
