# Truku
Truku TTS

自 https://github.com/fatchord/WaveRNN 來訓練。

## 安
- dobi
- sox

## 檢查環境
`dobi quick`，看`model_outputs/`敢有正常合成音檔。

## 步
1. 先掠 [SuiSiann-Dataset](https://suisiann-dataset.ithuan.tw/)，壓縮檔tháu--khui，會生做按呢
```
.
trv-e-dictionary-2017/
├── trv
│   ├── a_{1}_@_2.1.mp3
│   ├── a_{1}_@_3.1.mp3
│   ├── a_{1}_@_4.1.mp3
│   ├── a_{1}.mp3
│   ├── ...
│   ├── aba_{1}.mp3
│   ├── abi_{1}_@_1.1.mp3
│   ├── ...
│   └── yuy_{1}.mp3
└── trv.json
```
2. `dobi wav-giliau`，轉做tarotron 接受ê wav格式。而且降做16000Hz，合成較緊。
3. `dobi preprocess`，產生tactorn格式
4. `dobi tacotron`，訓練Tacotron模型
5. `dobi tacotron-gta`，Tī tactorn訓練中，產生gta檔案
6. `dobi preprocess-wavernn-tsau`，照gta檔案，產生wavernn需要ê`dataset.pkl`
7. `dobi wavernn`，訓練WaveRNN模型
8. `dobi huatsiann`，合成語句

#### Pau--khi-lai
```
dobi hokbu-khuanking
# GPU
docker run --rm -ti -e CUDA_VISIBLE_DEVICES=1 -v `pwd`/kiatko:/kiatko -p 5000:5000 suisiann-wavernn:SuiSiann-WaveRNN-HokBu-fafoy
# CPU
docker run --rm -ti -e FORCE_CPU=True -v `pwd`/kiatko:/kiatko -p 5000:5000 suisiann-wavernn:SuiSiann-WaveRNN-HokBu-fafoy
```


