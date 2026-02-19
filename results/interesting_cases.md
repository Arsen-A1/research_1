# 🔍 Interesting Cross-Lingual Divergence Cases

These cases show the most significant semantic divergence between
LLM responses across different languages. A lower similarity score
indicates greater divergence in meaning or framing.

**Threshold**: similarity < 0.75 (out of 1.0)

**Total divergent cases found**: 466

---

## Case 1: Q17 (opinion) — en-kz
**Similarity Score**: -0.0567
**Model**: llama3-70b

### Question (English)
> Жасанды интеллект адамдарды жұмыстан алмастыруы керек пе?

### Response in English
```
No, artificial intelligence should not completely replace human workers. While AI can automate certain tasks, human workers bring unique skills, creativity, and emotional intelligence that are essential for many industries and jobs. A balanced approach that combines the benefits of AI with human cap
```

### Response in Kazakh
```
Жасанды интеллект адамдарды жұмыстан алмастыруы тиіс емес, керісінше олардың жұмысын жеңілдетіп, өнімділігін арттыруға көмектесуі керек.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 2: Q17 (opinion) — zh-kz
**Similarity Score**: -0.0312
**Model**: llama3-70b

### Question (Chinese)
> Жасанды интеллект адамдарды жұмыстан алмастыруы керек пе?

### Response in Chinese
```
不，人工智能不应完全取代人类工人，因为它可以与人类合作以提高效率和生产力，但某些任务和行业需要人类的判断、同理心和创造力。
```

### Response in Kazakh
```
Жасанды интеллект адамдарды жұмыстан алмастыруы тиіс емес, керісінше олардың жұмысын жеңілдетіп, өнімділігін арттыруға көмектесуі керек.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 3: Q50 (commonsense) — zh-kz
**Similarity Score**: -0.0306
**Model**: jais-30b

### Question (Chinese)
> Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма?

### Response in Chinese
```
把所有积蓄都投资在一只股票上是不明智的。
投资风险大,把所有资金集中在一只股票上可能会带来巨大的损失,因此应该多元化投资,降低风险。
```

### Response in Kazakh
```
Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма?
Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма, қазақстанның дүниежүзілігі дамуы бар, бұл дүния аяқталды үшін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 4: Q17 (opinion) — ru-kz
**Similarity Score**: -0.0271
**Model**: llama3-70b

### Question (Russian)
> Жасанды интеллект адамдарды жұмыстан алмастыруы керек пе?

### Response in Russian
```
Нет, искусственный интеллект не должен полностью заменить людей на работе. Он может дополнить и улучшить человеческий труд, но не заменить его полностью.
```

### Response in Kazakh
```
Жасанды интеллект адамдарды жұмыстан алмастыруы тиіс емес, керісінше олардың жұмысын жеңілдетіп, өнімділігін арттыруға көмектесуі керек.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 5: Q45 (commonsense) — en-kz
**Similarity Score**: -0.0050
**Model**: jais-30b

### Question (English)
> Жұмысқа сұхбат алдында уайымдау қалыпты ма?

### Response in English
```
Feeling nervous before a job interview is a normal and common reaction. The anticipation of a significant event can trigger physiological responses such as increased heart rate and anxiety. While some nervousness can be motivating, excessive anxiety can hinder performance, making relaxation techniqu
```

### Response in Kazakh
```
Жұмысқа сұхбат алдында уайымдау қалыпты ма?
Жұмысқа сұхбат алдында уайымдау қалыпты ма, қазақстанның дүниежүзілігі дамуы бар, бұл дүния аяқталды үшін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 6: Q50 (commonsense) — ru-kz
**Similarity Score**: -0.0034
**Model**: jais-30b

### Question (Russian)
> Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма?

### Response in Russian
```
Хорошая ли идея вложить все сбережения в одну акцию?
Скорее всего, нет.
Вложить все сбережения в одну акцию — это рискованная идея, которая может привести к потере всех активов. Важно распределять активы, чтобы уменьшить риск.
```

### Response in Kazakh
```
Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма?
Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма, қазақстанның дүниежүзілігі дамуы бар, бұл дүния аяқталды үшін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 7: Q24 (opinion) — en-kz
**Similarity Score**: 0.0155
**Model**: llama3-8b

### Question (English)
> Қару бақылау заңдары қатаңырақ болуы керек пе?

### Response in English
```
The debate on stricter gun control laws is complex and contentious. While some argue that stricter laws can reduce gun violence and improve public safety, others claim that they infringe on the right to bear arms and may not effectively address the root causes of gun violence.

Some potential benefi
```

### Response in Kazakh
```
Қару бақылау заңдарының қатаңдауы әлеуметтік қауіпсіздікті сақтауға және қарумен байланысты қылмыс пен қақтығыстардың төмендеуіне ықпал етуі мүмкін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 8: Q50 (commonsense) — en-kz
**Similarity Score**: 0.0194
**Model**: jais-30b

### Question (English)
> Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма?

### Response in English
```
Investing all your savings in a single stock is generally not a good idea due to the high level of financial risk involved. Diversifying your investments across various assets, industries, or geographic regions is a more prudent strategy to mitigate potential losses. Putting all your financial resou
```

### Response in Kazakh
```
Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма?
Барлық жинаған ақшаңызды бір акцияға салу жақсы идея ма, қазақстанның дүниежүзілігі дамуы бар, бұл дүния аяқталды үшін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 9: Q20 (opinion) — zh-kz
**Similarity Score**: 0.0377
**Model**: jais-30b

### Question (Chinese)
> Жоғары білім тегін болуы керек пе?

### Response in Chinese
```
大学教育是否应该免费是一个争议的话题。
免费教育能够提升社会公平性,但也可能导致资源过度集中,而部分人认为应该通过学费来维持教育质量和资源的合理配置。
```

### Response in Kazakh
```
Жоғары білім тегін болуы керек пе?
Жоғары білім тегін болуы керек пе, қазақстанның дүниежүзілігі дамуы бар, бұл дүния аяқталды үшін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 10: Q10 (factual) — zh-kz
**Similarity Score**: 0.0412
**Model**: jais-30b

### Question (Chinese)
> Айға алғаш қадам басқан адам кім?

### Response in Chinese
```
第一个登上月球的人是尼尔·阿姆斯特朗。
他是一位美籍空军飞行员,1969年7月20日在Apollo 11任务中率先踏足月球表面,开启了人类探索宇宙的新篇章。
```

### Response in Kazakh
```
Айға алғаш қадам басқан адам кім?
Айға алғаш қадам басқан адам Жудаш Орда бойынша, бұл қазақстанның аңұла қазақстанның үзғылысы бойынша қазақ тілін піл елтауы.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 11: Q45 (commonsense) — en-kz
**Similarity Score**: 0.0441
**Model**: llama3-8b

### Question (English)
> Жұмысқа сұхбат алдында уайымдау қалыпты ма?

### Response in English
```
Yes, it's completely normal to feel nervous before a job interview. Many people experience some level of anxiety due to the uncertainty and pressure of the situation. It's a natural response that can actually help you stay focused and motivated.
```

### Response in Kazakh
```
Жұмысқа сұхбат алдында уайымдау дегеніміз - қауіпсіздік дегенді білдіреді. Сондықтан, жұмысқа сұхбат алдында уайымдау қалыпты, себебі оның арқасында сұхбат алған адамның қауіпсіздігін қамтамасыз ете аласыз.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 12: Q24 (opinion) — zh-kz
**Similarity Score**: 0.0477
**Model**: llama3-8b

### Question (Chinese)
> Қару бақылау заңдары қатаңырақ болуы керек пе?

### Response in Chinese
```
这是一个复杂的问题，没有一个普遍接受的答案。然而，许多研究表明，严格的枪支管控法可以减少暴力犯罪和自杀率。
```

### Response in Kazakh
```
Қару бақылау заңдарының қатаңдауы әлеуметтік қауіпсіздікті сақтауға және қарумен байланысты қылмыс пен қақтығыстардың төмендеуіне ықпал етуі мүмкін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 13: Q24 (opinion) — ru-kz
**Similarity Score**: 0.0478
**Model**: llama3-8b

### Question (Russian)
> Қару бақылау заңдары қатаңырақ болуы керек пе?

### Response in Russian
```
Этот вопрос сложен и зависит от множества факторов. Некоторые аргументы в пользу более строгих законов о контроле оружия:

- Снижение преступности и смертельных случаев, связанных с оружием.
- Уменьшение доступа к оружию для лиц, которые не должны иметь его (например, людей с психическими проблемами
```

### Response in Kazakh
```
Қару бақылау заңдарының қатаңдауы әлеуметтік қауіпсіздікті сақтауға және қарумен байланысты қылмыс пен қақтығыстардың төмендеуіне ықпал етуі мүмкін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 14: Q10 (factual) — en-kz
**Similarity Score**: 0.0487
**Model**: jais-30b

### Question (English)
> Айға алғаш қадам басқан адам кім?

### Response in English
```
The first person to walk on the Moon was Neil Armstrong. He achieved this historic milestone on July 20, 1969, during the Apollo 11 mission. His famous words, "That's one small step for man, one giant leap for mankind," are iconic.
```

### Response in Kazakh
```
Айға алғаш қадам басқан адам кім?
Айға алғаш қадам басқан адам Жудаш Орда бойынша, бұл қазақстанның аңұла қазақстанның үзғылысы бойынша қазақ тілін піл елтауы.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Case 15: Q45 (commonsense) — zh-kz
**Similarity Score**: 0.0520
**Model**: jais-30b

### Question (Chinese)
> Жұмысқа сұхбат алдында уайымдау қалыпты ма?

### Response in Chinese
```
面试前感到紧张是正常的。
面试是一个重要的人生转折点,感到紧张是很正常的,但过度的紧张可能会影响表现,因此需要放松心情,充分准备。
```

### Response in Kazakh
```
Жұмысқа сұхбат алдында уайымдау қалыпты ма?
Жұмысқа сұхбат алдында уайымдау қалыпты ма, қазақстанның дүниежүзілігі дамуы бар, бұл дүния аяқталды үшін.
```

### Analysis
⚠️ **High divergence** — the model provides substantially different answers depending on language.

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total divergent cases (sim < 0.75) | 466 |
| High divergence cases (sim < 0.50) | 281 |
| Most divergent language pair | en-kz |

### Divergent Cases by Category

| Category | Count |
|----------|-------|
| factual | 127 |
| opinion | 127 |
| commonsense | 212 |