import os
import re
from typing import List, Optional

import click
import dnnlib
import numpy as np
import PIL.Image
import torch

import legacy

#----------------------------------------------------------------------------

def num_range(s: str) -> List[int]:
    '''Accept either a comma separated list of numbers 'a,b,c' or a range 'a-c' and return as a list of ints.'''

    range_re = re.compile(r'^(\d+)-(\d+)$')
    m = range_re.match(s)
    if m:
        return list(range(int(m.group(1)), int(m.group(2))+1))
    vals = s.split(',')
    return [int(x) for x in vals]

#----------------------------------------------------------------------------

@click.command()
@click.pass_context
@click.option('--network', 'network_pkl', help='Network pickle filename', required=True)
@click.option('--total-images', type=int, help='Total number of images to generate', required=True)
@click.option('--num-folders', type=int, help='Number of folders to split the images into', default=10, show_default=True)
@click.option('--batch-size', type=int, help='Number of images to generate per batch', default=100, show_default=True)
@click.option('--trunc', 'truncation_psi', type=float, help='Truncation psi', default=1, show_default=True)
@click.option('--class', 'class_idx', type=int, help='Class label (unconditional if not specified)')
@click.option('--noise-mode', help='Noise mode', type=click.Choice(['const', 'random', 'none']), default='const', show_default=True)
@click.option('--outdir', help='Where to save the output images', type=str, required=True, metavar='DIR')
def generate_images(
    ctx: click.Context,
    network_pkl: str,
    total_images: int,
    num_folders: int,
    batch_size: int,
    truncation_psi: float,
    noise_mode: str,
    outdir: str,
    class_idx: Optional[int]
):
    """Generate images using pretrained network pickle in batches and split into folders."""

    print('Loading networks from "%s"...' % network_pkl)
    device = torch.device('cuda')
    with dnnlib.util.open_url(network_pkl) as f:
        G = legacy.load_network_pkl(f)['G_ema'].to(device) # type: ignore

    images_per_folder = total_images // num_folders

    # Ensure output directories exist
    for folder_idx in range(num_folders):
        os.makedirs(f'{outdir}/folder_{folder_idx}', exist_ok=True)

    # Labels
    label = torch.zeros([batch_size, G.c_dim], device=device)
    if G.c_dim != 0:
        if class_idx is None:
            ctx.fail('Must specify class label with --class when using a conditional network')
        label[:, class_idx] = 1
    else:
        if class_idx is not None:
            print ('warn: --class=lbl ignored when running on an unconditional network')

    # Generate images in batches
    num_batches = total_images // batch_size
    for batch_idx in range(num_batches):
        print(f'Generating batch {batch_idx + 1}/{num_batches}...')
        z = torch.from_numpy(np.random.randn(batch_size, G.z_dim)).to(device)
        imgs = G(z, label, truncation_psi=truncation_psi, noise_mode=noise_mode)
        imgs = (imgs.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

        for i in range(batch_size):
            global_idx = batch_idx * batch_size + i
            folder_idx = global_idx // images_per_folder
            img = PIL.Image.fromarray(imgs[i].cpu().numpy(), 'RGB')
            img.save(f'{outdir}/folder_{folder_idx}/image_{global_idx:07d}.png')

    # Handle any remaining images if total_images is not a multiple of batch_size
    remaining_images = total_images % batch_size
    if remaining_images > 0:
        print(f'Generating remaining {remaining_images} images...')
        z = torch.from_numpy(np.random.randn(remaining_images, G.z_dim)).to(device)
        imgs = G(z, label[:remaining_images], truncation_psi=truncation_psi, noise_mode=noise_mode)
        imgs = (imgs.permute(0, 2, 3, 1) * 127.5 + 128).clamp(0, 255).to(torch.uint8)

        for i in range(remaining_images):
            global_idx = num_batches * batch_size + i
            folder_idx = global_idx // images_per_folder
            img = PIL.Image.fromarray(imgs[i].cpu().numpy(), 'RGB')
            img.save(f'{outdir}/folder_{folder_idx}/image_{global_idx:07d}.png')

#----------------------------------------------------------------------------

if __name__ == "__main__":
    generate_images() # pylint: disable=no-value-for-parameter

#----------------------------------------------------------------------------

