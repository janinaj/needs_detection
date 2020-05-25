# download AutoPhrase
if [ ! -d "autophrase" ]; then
  curl -SL https://github.com/shangjingbo1226/AutoPhrase/archive/master.zip > autophrase.zip
  unzip autophrase.zip
  mv AutoPhrase-master autophrase
  rm autophrase.zip
  mv auto_phrase_cmd_args.sh autophrase/auto_phrase_cmd_args.sh
fi

run Autophrase
cp $1 autophrase/data/input.txt
if [ ! -d "../data/autophrase" ]; then
  mkdir ../data/autophrase
fi
cd autophrase
./auto_phrase_cmd_args.sh ../data/autophrase data/input.txt
rm data/input.txt
cd ..

perform priority needs detection
python priority_detection.py $1 data data/autophrase/AutoPhrase_multi-words.txt
