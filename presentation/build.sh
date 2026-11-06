#!/bin/sh
# Build the slides with XeLaTeX into build/.
# Three passes: the TikZ overlays (section dividers) use page positions recorded in the previous pass.
#   ./build.sh                 audience PDF  (build/main.pdf)
#   ./build.sh speaker-notes   notes PDF     (build/speaker-notes.pdf)
set -eu
cd "$(dirname "$0")"
target=${1:-main}
mkdir -p build
for pass in 1 2 3; do
    if ! xelatex -no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error \
        -output-directory=build "$target.tex" >/dev/null 2>&1; then
        tail -n 40 "build/$target.log"
        echo "xelatex failed on pass $pass" >&2
        exit 1
    fi
done
issues=$(grep -E 'Overfull|Missing character|undefined on input' "build/$target.log" || true)
[ -n "$issues" ] && printf '%s\n' "$issues"
count=$(printf '%s' "$issues" | grep -c . || true)
echo "build/$target.pdf: $(wc -c < "build/$target.pdf" | tr -d ' ') bytes, $count layout warning(s)"
