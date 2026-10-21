# FarRightFirewall

**Comparing the emotional and belief discourse of Charlie Kirk and Nick Fuentes (2020–2025) using Emotional Belief Analysis (EBA).**

This repository holds the coding manual, coding template, coded data, analysis scripts, and network visualizations for a project that samples podcast episodes from *The Charlie Kirk Show* and Nick Fuentes's *America First* and codes every statement for expressed emotion, belief, and topic. The goal is to map where the two figures' discourses overlap and where they diverge across the contemporary American right.

---

## Research approach

The project applies **Emotional Belief Analysis (EBA)**, a coding method built on the **Advocacy Coalition Framework (ACF)** (Fullerton, Gabehart & Weible). EBA identifies *expressed* emotions (emotion communicated through language, not felt affect) and pairs each one with the belief it is directed at, producing **emotion–belief dyads** that can be compared across actors and analyzed as networks.

Each coded statement captures:

| Field | Description |
| --- | --- |
| `n_actor`, `n_actor_aff`, `n_actor_pos` | Narrating actor, affiliation, and position (pro / anti / neutral) |
| `eb_actor`, `eb_actor_aff`, `eb_actor_pos` | Actor the emotion is ascribed to, affiliation, and position |
| `self_nar` | Whether the narrator is expressing their own emotion (yes / no) |
| `emot` | Emotion word and parent category, e.g. `concern (fear)`; implicit emotions are coded as the category alone, e.g. `(anger)` |
| `exp` | Explicit or implicit |
| `topic`, `stopic` | Topic from the project list, plus sub-topic |
| `blf` | Belief level: deep core (`identity`, `justice`), policy core (`topic`, `risk`, `benefit`, `others`), or secondary (`implementation`) |
| `cntxt` | Context needed to interpret the emotion (cause, target, hat-tipping, devil shift, etc.) |

**Emotion categories (8):** affinity, compassion, confidence, contentment (positive) · anger, carelessness, dismay, fear (negative).

**Topics (20):** immigration & border security · Trump & MAGA politics · Ukraine war & U.S. foreign aid · free speech · anti-"woke" culture · LGBTQ issues · mainstream media · COVID-19 & government overreach · women's roles & feminism · Israel policy · abortion · China · Christian nationalism · economic policy · election integrity & voter fraud · white nationalism · intra-right feuds · men's rights · Russia · NATO.

The full rules, thesaurus of emotion words, and belief-system definitions are in the coding manual.

---

## Repository contents

### Method
| File | Description |
| --- | --- |
| `2026 EBA Coding Manual_FarRight.docx` | EBA coding guidelines adapted for this project: coding units, emotion thesaurus, explicit vs. implicit coding, belief system definitions |
| `Appendix A.pdf`, `Appendix B.pdf`, `Appendix C.pdf` | Supplementary appendices |
| `coding_results_template_farright.xlsx` | Blank 18-column template all coded output follows |

### Data
| File | Description |
| --- | --- |
| `coding_results_farright.xlsx` | Coded statements |
| `kirk_coding_by_year.xlsx` | Kirk statements, one sheet per year (2020–2025) |
| `fuentes_coding_by_year_statements.xlsx` | Fuentes statements, one sheet per year (2020–2025) |
| `eba_summary_table.xlsx` | Annual summary comparing Fuentes and Kirk by emotion, belief, and topic |

### Code
| File | Description |
| --- | --- |
| `charlie_kirk_episodes_by_year.py` | Pulls the full episode list for *The Charlie Kirk Show* from its official RSS feed and groups titles, dates, and links by year, to build the sampling frame |
| `transcribe.py` | Batch transcription of podcast audio with Whisper (local model or OpenAI API) |

### Visualizations
| File | Description |
| --- | --- |
| `tripartite_clean_final.html` | Interactive actor × topic × dyad network with degree and betweenness centrality |
| `contrast_network_v4.html` | Interactive contrast network placing topics and dyads on a Kirk-to-Fuentes axis by proportional use |

Both visualizations are self-contained D3 pages; open them in a browser.

---

## Pipeline

1. **Sample** podcast episodes for each speaker across 2020–2025. For Kirk, list every episode by year from the show's RSS feed (standard library only, no installs needed):
   ```bash
   python3 charlie_kirk_episodes_by_year.py                                   # plain text to the terminal
   python3 charlie_kirk_episodes_by_year.py --format csv -o kirk_episodes.csv  # CSV: Year, Date, Title, Link
   python3 charlie_kirk_episodes_by_year.py --format markdown > kirk_episodes.md
   ```
   Each episode's link is its audio file where the feed provides one, otherwise the episode page. Use `--feed-url` to point at a different feed.
2. **Transcribe** audio to text:
   ```bash
   pip install openai-whisper    # requires ffmpeg on your system
   python transcribe.py --input ./audio --output ./transcripts --mode local --model medium
   ```
   Or use the API: `--mode api --api_key YOUR_KEY`. Already-transcribed files are skipped unless `--no-resume` is passed.
3. **Code** each transcript statement-by-statement following the manual, into the template format. Exact duplicate statements are removed.
4. **Aggregate** coded statements by speaker and year into the by-year workbooks and summary table.
5. **Analyze and visualize** emotion–belief dyads as networks.

---

## Reading the networks

- **Tripartite network.** Actors, topics, and dyads (emotion × belief) are the three node types. Edge weight is co-occurrence. Because both actors connect to most topics, modularity is close to zero by construction; degree centrality, betweenness centrality, and discourse balance are the informative measures.
- **Contrast network.** Each topic and dyad is positioned by a Fuentes-ratio, `fp / (kp + fp)`, where `kp` and `fp` are each speaker's proportional use. 0 means used only by Kirk, 0.5 equal proportional use, 1 only by Fuentes. Proportions correct for the two speakers contributing different numbers of statements.

---

## A note on the material

This project studies political discourse that includes white nationalist, antisemitic, and other extremist rhetoric. Coded statements reproduce that language verbatim for analytic purposes. Inclusion in the dataset does not represent endorsement by the researchers.

---

## Authors

- **Kayla M. Gabehart**, Michigan Technological University · kgabehar@mtu.edu

EBA method: Allegra H. Fullerton, Kayla M. Gabehart, and Christopher M. Weible.

## References

- Fullerton, A. H., & Gabehart, K. M. (2026). Emotional Belief Analysis coding guidelines.
- Jenkins-Smith, H. C., & Sabatier, P. A. (1993). Methodological appendix: Measuring longitudinal change in elite beliefs using content analysis of public documents. In *Policy Change and Learning: An Advocacy Coalition Approach*. Westview Press.
- Nohrstedt, D., Ingold, K., Weible, C. M., Koebele, E. A., Olofsson, K. L., Satoh, K., & Jenkins-Smith, H. C. (2023). The Advocacy Coalition Framework: Progress and emerging areas. In C. M. Weible (Ed.), *Theories of the Policy Process* (5th ed.). Routledge.
- Sabatier, P. A., & Jenkins-Smith, H. C. (1999). The Advocacy Coalition Framework: An assessment. In P. A. Sabatier (Ed.), *Theories of the Policy Process*. Westview Press.

## License

No license has been selected yet. Until one is added, all rights are reserved by the authors.
