---
name: facebook-marketplace
description: Publica anúncios no Facebook Marketplace pelo Claude no Chrome (extensão), a partir de ordens de publicação do usuário (lote, preço, região, CEP, fotos). Use quando o usuário pedir para postar, publicar, republicar ou verificar anúncios no Facebook Marketplace, ou invocar /facebook-marketplace.
---

# Facebook Marketplace — publicação pelo Claude no Chrome

O usuário abre esta skill e dá **ordens de publicação**. Eu executo no Chrome (ferramentas `mcp__claude-in-chrome__*`, na conta já logada do usuário) e registro o resultado.

## 1. Receber a ordem

Cada ordem precisa destes dados. Se faltar algo, **pergunte antes de publicar**; nunca invente preço, metragem, CEP ou texto.

| Campo | Exemplo |
|---|---|
| Código/lote | PRAIA-GRANDE |
| Categoria | Imóvel à venda / terreno |
| Região (cidade/UF) | Joinville - SC |
| CEP / localização | 89201-001 |
| Preço | 28000 |
| Área (m²) | 360 |
| Título | Terreno 360m² Praia Grande |
| Descrição | texto fornecido pelo usuário |
| Fotos | caminho local, pasta do Drive ou arte já gerada |
| Quantidade / ritmo | ex.: 2 por dia, espaçadas |

Fontes aceitas para os lotes: lista colada na conversa, planilha do Google Sheets e fotos do Drive (conector do Google Drive). Confirme o resumo da ordem em uma linha antes de começar a lote grande.

## 2. Preparação

1. Carregue as ferramentas do Chrome com ToolSearch (`mcp__claude-in-chrome__`), liste as abas abertas e trabalhe em uma aba nova.
2. Confirme que o Facebook está logado. Se pedir login, senha, 2FA ou CAPTCHA: **pare e avise o usuário**; nunca digite credenciais.
3. Leia `data/publications.json` (se existir) para não duplicar lote + região já publicados.

## 3. Fluxo de publicação (repetir por anúncio)

1. Abra `https://www.facebook.com/marketplace/create` e escolha o tipo (item, imóvel/aluguel) conforme a categoria da ordem.
2. Envie as fotos pelo input de arquivo (`type=file`); aguarde o upload terminar.
3. Preencha título, preço, categoria, descrição e localização/CEP **exatamente como na ordem**. A localização pode ser sobrescrita pelo padrão da conta: confira na captura e redigite se necessário.
4. Tire screenshot e confira todos os campos com a ordem antes do botão final.
5. Clique em **Avançar / Publicar**. Não aceite impulsionamento, anúncio pago ou qualquer cobrança.
6. Confirme que o anúncio aparece em "Seus anúncios" (Marketplace > Vender > Seus anúncios) e copie a URL.
7. Registre o resultado (seção 5) e siga para o próximo, respeitando o espaçamento.

Dica: use `find`/refs para campos em vez de coordenadas; o layout do Facebook muda. Use `browser_batch` quando possível.

## 4. Regras de segurança e ritmo

- **Parar e avisar** diante de CAPTCHA, verificação de conta, aviso de violação, limite de publicações ou pedido de pagamento. Não contornar.
- Não pagar nada nem aceitar impulsionamento sem "sim" explícito do usuário naquele anúncio.
- O mesmo lote em várias cidades pode ser lido como spam: espaçar as postagens (padrão sugerido: 1–2 lotes por dia, com intervalo entre anúncios) e variar o texto só se o usuário pedir.
- Exclusões, edições em massa ou republicação de anúncio existente só com ordem explícita.
- Nunca inventar dados do anúncio; usar só o que o usuário forneceu.

## 5. Histórico

Mantenha `data/publications.json` nesta pasta da skill, um registro por anúncio:

```json
{"codigo":"PRAIA-GRANDE","regiao":"Joinville - SC","cep":"89201-001","preco":28000,"area":360,"status":"published|blocked|draft","url":"","data":"2026-10-08","obs":""}
```

Atualize após cada tentativa, inclusive as bloqueadas, com o motivo em `obs`.

## 6. Relatório final

Ao terminar, responda curto: quantos publicados, links, o que ficou bloqueado e por quê, e o que falta da ordem. Se for uma rotina agendada, o app e o Chrome precisam estar abertos com a extensão conectada.

## Pendências desta versão

Esta skill foi recriada a partir do resumo da sessão da OLX, sem o texto da skill original. Na primeira execução, anote aqui os detalhes reais do formulário do Facebook (nomes de campos, categoria exata de terreno, onde a localização é pedida) para as próximas rodadas ficarem mais rápidas.
