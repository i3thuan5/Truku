# Truku

Truku TTS

自 <https://github.com/fatchord/WaveRNN> 來訓練。

## 安

- [dobi](https://github.com/dnephin/dobi)
- [docker](https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/)
- [docker-compose](https://docs.docker.com/compose/install/)
- 設定docker權限`sudo usermod -aG docker $USER`

## 步

1. `dobi tsuan-pianma`，wave降做16kHz，合成較緊。
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
