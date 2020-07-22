#!/bin/bash
# Downloads support annotation data.
# Project page: https://blablablab.si.umich.edu/projects/support/

git_root_dir="$(git rev-parse --show-toplevel)"
target_dir="$git_root_dir/support_classification/data"
echo "Will download data to '$target_dir'."

if [ ! -d "$target_dir" ]; then
    mkdir -p "$target_dir"
fi
cd "$target_dir" || exit 1

wget https://blablablab.si.umich.edu/projects/support/data/crowdflower-support-annotations.csv.gz || exit 1
gunzip crowdflower-support-annotations.csv.gz
chmod a-w crowdflower-support-annotations.csv
echo "Finished."
pwd

