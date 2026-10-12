#!/usr/bin/env bash
# GEO-AAO 一键推送：台式机 -> 阿里云VPS中继 -> GitHub（绕过本机网络限制）
# 用法：在本目录执行 bash push-vps.sh
set -e
VPS_KEY="C:/Users/14429/.ssh/id_rsa.pem"
VPS_USER="ubuntu@119.45.16.249"
REPO="1124gong/GEO-AAO"

cd "$(dirname "$0")"

if [ -z "$(git log --oneline -1 2>/dev/null)" ]; then echo "没有提交记录"; exit 1; fi

echo "[1/3] 打包 bundle ..."
git bundle create /tmp/geo-aao.bundle main

echo "[2/3] 上传 VPS ..."
scp -q -i "$VPS_KEY" -o StrictHostKeyChecking=no /tmp/geo-aao.bundle "$VPS_USER":/tmp/geo-aao.bundle
rm -f /tmp/geo-aao.bundle

echo "[3/3] VPS 中继推送 ..."
ssh -i "$VPS_KEY" -o StrictHostKeyChecking=no "$VPS_USER" '
set -e
TOK=$(cat ~/.github_token)
rm -rf /tmp/geo-aao-repo
git clone -q -b main /tmp/geo-aao.bundle /tmp/geo-aao-repo
cd /tmp/geo-aao-repo
for i in 1 2 3 4 5; do
  if git push -q https://1124gong:$TOK@github.com/'"$REPO"'.git main; then break; fi
  echo "  重试 $i ..."; sleep 10
done
curl -s -m 15 "https://api.github.com/repos/'"$REPO"'/git/refs/heads/main" | grep -o "\"sha\": *\"[a-f0-9]\{7\}\"" && echo "推送成功"
rm -rf /tmp/geo-aao-repo /tmp/geo-aao.bundle'

echo "完成：https://github.com/$REPO （Pages 1-2 分钟后自动更新）"
