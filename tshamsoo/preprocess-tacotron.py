import argparse
from multiprocessing import Pool, cpu_count
from os.path import splitext, basename
from pathlib import Path
import pickle
from typing import Union

from utils import hparams as hp
from utils.display import *
from utils.dsp import *
from utils.files import get_files
from utils.paths import Paths
from csv import DictReader


# Helper functions for argument types
def valid_n_workers(num):
    n = int(num)
    if n < 1:
        raise argparse.ArgumentTypeError(
            '%r must be an integer greater than 0' % num)
    return n


parser = argparse.ArgumentParser(
    description='Preprocessing for WaveRNN and Tacotron')
parser.add_argument(
    '--path', '-p', type=Path,
    help='directly point to dataset path (overrides hparams.wav_path'
)
parser.add_argument(
    '--extension', '-e', metavar='EXT', default='.wav',
    help='file extension to search for in dataset folder'
)
parser.add_argument(
    '--num_workers', '-w', metavar='N', type=valid_n_workers,
    default=cpu_count() - 1,
    help='The number of worker threads to use for preprocessing'
)
parser.add_argument(
    '--hp_file', metavar='FILE', default='hparams.py',
    help='The file to use for the hyperparameters'
)
args = parser.parse_args()

hp.configure(args.hp_file)  # Load hparams from file
if args.path is None:
    args.path = hp.wav_path

extension = args.extension
path = args.path


def truku(path: Union[str, Path], wav_files):
    u_tihleh = set()
    for sootsai in wav_files:
        u_tihleh.add(basename(sootsai))
    text_dict = {}

    with open(path / '..' / 'Truku.csv', encoding='utf-8') as f:
        for 行 in DictReader(f):
            檔名 = 'E-TV001-{:0>4}'.format(行['錄音編號'])
            if 檔名 + '.wav' in u_tihleh:
                text_dict[檔名] = 行['太魯閣語'].lower()

    return text_dict


def convert_file(path: Path):
    y = load_wav(path)
    peak = np.abs(y).max()
    if hp.peak_norm or peak > 1.0:
        y /= peak
    mel = melspectrogram(y)
    if hp.voc_mode == 'RAW':
        quant = encode_mu_law(
            y, mu=2**hp.bits) if hp.mu_law else float_2_label(y, bits=hp.bits)
    elif hp.voc_mode == 'MOL':
        quant = float_2_label(y, bits=16)

    return mel.astype(np.float32), quant.astype(np.int64)


def process_wav(path: Path):
    wav_id = path.stem
    m, x = convert_file(path)
    np.save(paths.mel / f'{wav_id}.npy', m, allow_pickle=False)
    np.save(paths.quant / f'{wav_id}.npy', x, allow_pickle=False)
    return wav_id, m.shape[-1]


wav_files = get_files(path, extension)
paths = Paths(hp.data_path, hp.voc_model_id, hp.tts_model_id)

print(f'\n{len(wav_files)} {extension[1:]} files found in "{path}"\n')

if len(wav_files) == 0:

    print('Please point wav_path in hparams.py to your dataset,')
    print('or use the --path option.\n')

else:
    if not hp.ignore_tts:
        text_dict = truku(path, wav_files)
        with open(paths.data / 'text_dict.pkl', 'wb') as f:
            pickle.dump(text_dict, f)
    print(text_dict)

    u_wav_files = []

    for im in wav_files:
        if splitext(basename(im))[0] in text_dict:
            u_wav_files.append(im)

    print(f'\n{len(u_wav_files)} {extension[1:]} files found in "{path}"\n')

    # (oo')

    n_workers = max(1, args.num_workers)

    simple_table([
        ('Sample Rate', hp.sample_rate),
        ('Bit Depth', hp.bits),
        ('Mu Law', hp.mu_law),
        ('Hop Length', hp.hop_length),
        ('CPU Usage', f'{n_workers}/{cpu_count()}')
    ])

    pool = Pool(processes=n_workers)
    dataset = []

    for i, (item_id, length) in enumerate(
        pool.imap_unordered(process_wav, u_wav_files), 1
    ):
        dataset += [(item_id, length)]
        bar = progbar(i, len(u_wav_files))
        message = f'{bar} {i}/{len(u_wav_files)} '
        stream(message)

    with open(paths.data / 'dataset.pkl', 'wb') as f:
        pickle.dump(dataset, f)

    print(
        '\n\n'
        'Completed. '
        'Ready to run "python train_tacotron.py" '
        'or "python train_wavernn.py". \n'
    )
