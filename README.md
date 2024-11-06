# Truku

Truku TTS

自 <https://github.com/fatchord/WaveRNN> 來訓練。

## 安

- [dobi](https://github.com/dnephin/dobi)
- [docker](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/)
- 設定docker權限`sudo usermod -aG docker $USER`

## 步

1. 先用`dobi liah-giliau`，會掠語料，好勢會生做按呢

```plain
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

2. `dobi tsuan-pianma`，1. 轉做tarotron 接受ê wav格式。2. Tok頭尾無聲ê部份，tacotron較會收斂。3. 而且wave降做16000Hz，合成較緊。

```plain
trv-e-dictionary-2017-wav/
├── trv
│   ├── a_{1}_@_2.1.mp3.wav
│   ├── a_{1}_@_3.1.mp3.wav
│   ├── a_{1}_@_4.1.mp3.wav
│   ├── a_{1}.mp3.wav
│   ├── ...
│   ├── aba_{1}.mp3.wav
│   ├── abi_{1}_@_1.1.mp3.wav
│   ├── ...
│   └── yuy_{1}.mp3.wav
└── trv.json
```

3. `dobi preprocess-tacotron`，產生tactorn格式
4. `dobi tacotron`，訓練Tacotron模型
5. `dobi tacotron-gta`，Tī tacotron訓練中，產生gta檔案
6. `dobi preprocess-wavernn`，照gta檔案，產生wavernn需要ê`dataset.pkl`
7. `dobi wavernn`，訓練WaveRNN模型
8. `dobi huatsiann`，合成語句

### Pau--khi-lai

```bash
dobi hokbu-khuanking
# GPU
docker run --rm -ti -e CUDA_VISIBLE_DEVICES=1 -v `pwd`/kiatko:/kiatko -p 5000:5000 suisiann-wavernn:SuiSiann-WaveRNN-HokBu-fafoy
# CPU
docker run --rm -ti -e FORCE_CPU=True -v `pwd`/kiatko:/kiatko -p 5000:5000 suisiann-wavernn:SuiSiann-WaveRNN-HokBu-fafoy
```
