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
├── 0.2
│   ├── ImTong
│   │   ├── SuiSiann_0001.wav
│   │   ├── SuiSiann_0002.wav
│   │   ├── SuiSiann_0003.wav
│   │   ├── SuiSiann_0004.wav
│   │   ├── SuiSiann_0005.wav
│   │    ...
│   └── SuiSiann.csv
├── dobi.yaml
├── Dockerfile
...
```
2. `dobi suisiann-giliau`，轉做22050Hz
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

