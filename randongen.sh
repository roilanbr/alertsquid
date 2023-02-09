#!/bin/bash

# Simular conección web 

# export http_proxy=http://127.0.0.1:3128
export http_proxy=

while true
  do
    sex="http://www.sex.cu"
    porn="http://www.porn.cu"
    xvideo="http://www.xvideo.cu"
    rbr="http://www.rbr.cu"
    virus="http://www.virus.cu"
    info="http://www.info.cu"
    tecno="http://www.tecno.cu"
    game="http://www.game.cu"
    video="http://www.video.cu"
    ip1="http://111.0.0.1/sex"
    ip2="http://122.0.0.2/porn"
    ip3="http://133.0.0.3/virus"
    ip4="http://144.0.0.4/game"
    ip5="http://155.0.0.5/video"
    url=($sex $porn $xvideo $rbr $virus $info $tecno $game $video $ip1 $ip2 $ip3 $ip4 $ip5)
    ranNum=$[RANDOM%${#url[@]}]
    # curl -s -m 1 ${url[$ranNum]}
    curl -m 1 ${url[$ranNum]}
    sleep 2
done
exit 0