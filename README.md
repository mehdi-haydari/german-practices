# Deutsch A2 practice journal

This public repository contains the website source and learner practice data. The learner's original German answers, corrections, and practice notes are publicly visible here. The coursebook PDF, full transcription, and private workspace notes are excluded.

The journal follows this navigation: **lesson index → lesson page → grouped practice page**. Lesson 9 → C2.a collects Fragen A and B together. The previous per-question links redirect to the matching questions on that page.

## GitHub Pages

Journal: https://german-practices.mehdiheydari.dev/

The workflow in `.github/workflows/pages.yml` builds the site at the custom domain root and deploys the generated `dist/` directory after pushes to `main`. The `CNAME` file is copied into the Pages artifact. Repository Settings → Pages uses **GitHub Actions** as the publishing source.

## Update the journal

1. Add or update the relevant question in `practices.json`, preserving exact submitted wording. Append retries rather than overwriting earlier answers.
2. Keep record IDs unchanged; they maintain redirects to question anchors on the grouped practice page. Keep lesson and grouped-practice paths stable.
3. Group new questions under the appropriate book practice in `build.py`.
4. For a local root-path preview, run `python3 build.py`. Run `python3 check.py` and `node --check app.js` after building.
5. Push changes to `main`; GitHub Actions publishes the updated Pages site.

The generated site is read-only for visitors. Keep clarified meanings, teacher examples, and independent learner submissions distinct, and avoid claims of mastery based only on immediate guided answers.
