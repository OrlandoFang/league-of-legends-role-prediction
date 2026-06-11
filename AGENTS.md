# AGENTS.md

## Cursor Cloud specific instructions

This repository is a **Jekyll GitHub Pages site** (a data-analysis writeup using the
remote `pages-themes/cayman` theme). The only service is the Jekyll dev server.

### Running the site (dev mode)
- Serve locally with: `bundle exec jekyll serve --host 0.0.0.0 --port 4000 --livereload`
- The site is then reachable at `http://localhost:4000/`.
- Auto-regeneration is enabled: editing `README.md` / `_config.yml` triggers a rebuild
  and the change is served immediately (no restart needed).
- First build downloads the remote Cayman theme from GitHub, so network access is required.
  GitHub Metadata warnings about "No GitHub API authentication" are expected and harmless.

### Bundler version gotcha (important)
- Dependencies are managed via a `Gemfile` pinned to `github-pages "~> 232"` (this mirrors
  the live GitHub Pages build: Jekyll 3.10, kramdown 2.4, etc.).
- The `github-pages` gem requires `bundler < 3`. A newer Bundler (e.g. 4.x) makes the
  resolver silently downgrade to the ancient `github-pages 170` / `jekyll 3.6.2`, which then
  crashes at runtime with `cannot load such file -- rexml/...`.
- Always use **Bundler 2.5.x**. Run bundler commands as `bundle _2.5.23_ ...` (the
  committed `Gemfile.lock` pins `BUNDLED WITH 2.5.23`, so a plain `bundle install` also works).

### Build / lint / test
- There is no test suite or linter in this repo (it is a static content site).
- "Build" = the Jekyll generation step, exercised by `bundle exec jekyll build` or by the
  `jekyll serve` command above (output goes to the gitignored `_site/`).
