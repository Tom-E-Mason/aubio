#! /usr/bin/env bash

set -e
#set -x

WAFVERSION=2.0.21
WAFTARBALL=waf-$WAFVERSION.tar.bz2
WAFURL=https://waf.io/$WAFTARBALL
WAFUPSREAMKEYCOMMIT=edde20a6425a5c3eb6b47d5f3f5c4fbc93fed5f4
WAFUPSTREAMKEY=https://gitlab.com/ita1024/waf/raw/$WAFUPSREAMKEYCOMMIT/utils/pubkey.asc

WAFBUILDDIR=`mktemp -d`

function cleanup () {
  rm -rf $WAFBUILDDIR
}

trap cleanup SIGINT SIGTERM

function download () {
  ( [[ -n `which wget` ]] && wget -qO $1 $2 ) || ( [[ -n `which curl` ]] && curl -so $1 $2 )
}

function checkwaf () {
  download $WAFTARBALL.asc $WAFURL.asc
  if [[ -z `which gpg` ]]
  then
    echo "Warning: gpg not found, not verifying signature for $WAFTARBALL"
  else
    download - $WAFUPSTREAMKEY | gpg --import
    gpg --verify $WAFTARBALL.asc || exit 1
  fi
}

function fetchwaf () {
  download $WAFTARBALL $WAFURL
  checkwaf
}

function buildwaf () {
  tar xf $WAFTARBALL
  pushd waf-$WAFVERSION
  NOCLIMB=1 python waf-light --tools=c_emscripten $*
  popd
}

pushd $WAFBUILDDIR
fetchwaf
buildwaf
popd

cp -prv $WAFBUILDDIR/waf-$WAFVERSION/waf "$PWD"
chmod +x waf

cleanup
