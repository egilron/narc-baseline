# Modellering ut fra nye narc-data

### Elementer
- Dataene i Petters repo for annoteringene
- Konvertering Brat til jsonlines: Tollefs pull request
- Std jsonlines videre til wl-coref formatet med skriptene i mitt ncc
-  Modellering fra min fork av wl-coref

## Nytt repo:  narc-baseline på github.com
Enn så lenge på min bruker. Regner med at det skal inn til ltg-oslo etter hvert.

**Setup**: 
- Trekke ned narc og wl-coref fork
- Bygge inn min kode fra ncc og Tollefs pull request 



## Publisering av dataene
Regner med at vi ikke skal publisere dataene ennå, så jeg tenker jeg lar det være et privat repo enn så lenge.

## Logg
Mandag 6. juli: Dataene konverteres OK

**Tirsdag 7. juli:**
Trent på FOX med bare de ferdigstilte Bokmål-dataene. 
Evaluert på Dev splitt 80-10-10
```
[POC_000]
bert_model = "/fp/homes01/u01/ec-egilron/transformers/nb-bert-base"
f1: 0.47451, p: 0.57348, r: 0.40467:

[POC_001]
bert_model = "/fp/homes01/u01/ec-egilron/transformers/221"
f1: 0.52724, p: 0.60626, r: 0.46645:

[POC_002]
bert_model = "xlm-roberta-base"
f1: 0.55916, p: 0.56750, r: 0.55106:

[POC_003]
bert_model = "bert-base-multilingual-cased"
f1: 0.48878, p: 0.55390, r: 0.43736:

```