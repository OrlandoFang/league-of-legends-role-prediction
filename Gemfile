source "https://rubygems.org"

# Run the site locally with the same dependencies GitHub Pages uses.
# github-pages bundles jekyll, jekyll-remote-theme, and the other GitHub Pages
# plugins at versions matching the live GitHub Pages build environment.
gem "github-pages", "~> 232", group: :jekyll_plugins

# Windows and JRuby do not include zoneinfo files, so bundle the tzinfo-data gem
# and associated library.
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance-booster for watching directories on Windows
gem "wdm", "~> 0.1", :platforms => [:mingw, :x64_mingw, :mswin]

# Lock `http_parser.rb` gem to `v0.6.x` on JRuby builds since newer versions
# require Ruby C extensions that JRuby does not support.
gem "http_parser.rb", "~> 0.6.0", :platforms => [:jruby]
