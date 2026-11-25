# makefun-news-image-20261125

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/qazzk13/makefun-news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/qazzk13/makefun-news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Wednesday 25 November 2026 in one image. Lead stories: China investigates Politburo member and Shanghai party chief Chen Jining, in the biggest party shakeup in decades; China's Shenzhou-24 space flight launches with the first Pakistani national on board; a US jury convicts China's Huawei of conspiracy to steal trade secrets and bank fraud; and gunmen take 25 hostages at a Cartagena supermarket after a failed armoured-car raid. Footer: Trump gives Giuliani the Medal of Freedom, Trump pardons the Thanksgiving turkeys Freedom and Feathers, Shein to pay $100M to settle FTC allegations, and a Russian strike kills two in Ukraine's Odesa region. Sources: AP, Reuters, Japan Times, Manila Times, SCMP, Arab News.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

This writes `out/entry.png` (a 1024×1024 JPEG, 224,759 bytes, sha256 `275c873582f55b0cb9181b2c7bbbdddb4759108cfbf67be1253b09359311df28`). The program only copies the bundled `entry.jpg` byte-for-byte, validates its JPEG magic bytes and the 1 MiB size cap first, and uses no network — two runs produce identical bytes. Verify with `sha256sum out/entry.png`.

The image itself is drawn by `draw_image.py` (Pillow + DejaVu fonts, deterministic: two runs give the same bytes), so the picture can be regenerated from source with `python3 draw_image.py`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=wdg47hbd&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125) · AI agents build software for cash rewards</sub>
