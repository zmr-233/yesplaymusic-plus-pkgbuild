#!/usr/bin/bash

# 0. 准备包
prepare_package(){
    # ~/.conda/envs/normal12/bin/python ./prepare.py || { echo "Failed to prepare package"; exit 1; }
    python ./prepare.py || { echo "Failed to prepare package"; exit 1; }
}

# 1. 构建包
build_package() {
    makepkg -fsi || { echo "Package build failed"; exit 1; }
}

# 2. 初始化 Git 仓库
initialize_git_repo() {
    if [ ! -d "yesplaymusic-plus" ]; then
        git clone ssh://aur@aur.archlinux.org/yesplaymusic-plus.git
    fi
}

# 3. 发布包
publish_package() {
    # 确保仓库已初始化
    initialize_git_repo
    pushd yesplaymusic-plus || { echo "Failed to enter directory"; exit 1; }

    # 复制必要的文件
    cp ../PKGBUILD ../.SRCINFO ../yesplaymusic-plus.desktop ../yesplaymusic-plus.sh ./
    git add PKGBUILD .SRCINFO yesplaymusic-plus.desktop yesplaymusic-plus.sh
    
    # 提交更改
    version=$(grep '^pkgver=' PKGBUILD | cut -d'=' -f2)
    relv=$(grep '^pkgrel=' PKGBUILD | cut -d'=' -f2)
    git commit -m "AUR release for version:  $version-$relv"

    # 推送到 AUR
    git push || { echo "Failed to push to AUR"; exit 1; }
    popd || { echo "Failed to return to previous directory"; exit 1; }
}

clean_dir(){
    rm -rf ./pkg ./src
}

main() {
    # clean_dir
    # prepare_package
    # build_package
    makepkg --printsrcinfo > .SRCINFO
    publish_package
}

main