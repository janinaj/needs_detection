# download AutoPhrase
if [ ! -d "autophrase" ]; then
  curl -SL https://github.com/shangjingbo1226/AutoPhrase/archive/master.zip > autophrase.zip
  unzip autophrase.zip
  mv AutoPhrase-master autophrase
  rm autophrase.zip
  mv auto_phrase_cmd_args.sh autophrase/auto_phrase_cmd_args.sh
fi

if [ ! -d "../{$1}" ]; then
  mkdir ../$1
fi

run Autophrase
cp $1.txt autophrase/data/$1.txt
if [ ! -d "../{$1}/autophrase" ]; then
  mkdir ../$1/autophrase
fi
cd autophrase
./auto_phrase_cmd_args.sh ../$1/autophrase data/$1.txt
rm data/$1.txt
cd ..

# perform priority needs detection
python priority_detection.py $1.txt $1 $1/autophrase/AutoPhrase_multi-words.txt
