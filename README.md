# Diachronic-Chinese-Treebank
## Overview
This is my project for Option B Computational Linguistics. 
It aims to build a Chinese diachronic treebank with data from 1950-2010.

| Period of Time  | Number of Characters including punctuation characters | Number of Characters excluding punctuation characters |tokens | types | sentences
| ------------- | ------------- |-----------------|--------| -------| ----------
| 1950-1965          | 245,509   | 220,000   | 148,228 |21,975 | 7,195
| 1966-1976          |  48,953   |  43,286    | 30,564 |6,709 | 1,397
|  1978-1999         | 351,048 |  315,014         | 211,408 | 29,161 | 9,220
|  2000-2010         |  343,374        |   309,192           | 203,879 | 28,187 | 9,610
| Total | 988,888|887,492| 594,079 | 56,823 | 27,422
* There are 5703 characters in the sample corpus (including punctuation characters).
* There are 5062 characters in the sample corpus (excluding punctuation characters).

Aiming to build a balanced corpus, this corpus is designed with reference to the State Language Committee Modern Chinese Corpus(a diachronic corpus) and Lancaster Corpus of Mandarin Chinese (a synchronic corpus) (changes are made because of the litmitation of available data), and the texts are sampled from the following categories.
| Domain	|Percentage	|Literature	|Percentage	|Date	|Percentage|
|-------|-----------|------------|----------|------|----------|
| Press Reportage/Editorials|	30%	|General/Romantic Fiction|	50%	|1950-1965|	25%|
| Literature	|50%	|Prose	|30%	|1966-1976	|5%|
| Others	|20%	|Others|	10%	|1977 -1999	|35%|
| | |Science/Detective Fiction|	10%	|2000 -2010	|35%|

<sub> Press reportage and editorials are mainly from People's Daily and Reference News, two representative Chinese newspapers;
 others in general includes Chinese government report each year and books in other fields including history, philosophy, and academic theories;
 others in literature inlcudes biographies, non-fiction novel, and literary criticism.</sub>
