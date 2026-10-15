"""Shared helper for patches that append features to biome JSON.

A biome patch that only mounts a placed feature to a set of biomes is the same
code in every version, differing in the source directory and the feature ids. This
helper keeps the code here and leaves those two values in the patch:

    from patch_lib import biomes

    TYPE = 'json'
    reference_file, process_multi = biomes.add_features(
        Path('vanilla_biomes/1_20_2_overworld'), 4,
        'floating_island:end_gateway_return_overworld')

    # one feature per biome
    reference_file, process_multi = biomes.add_features(
        Path('vanilla_biomes/1_19_4_nether'), 4,
        lambda target: ['floating_island:end_gateway_return_warped' if target.stem == 'warped_forest'
                        else 'floating_island:end_gateway_return_nether'])
"""

from pathlib import Path
import typing as ty


def add_features(
        source: Path,
        step: int,
        features: ty.Union[str, ty.List[str], ty.Callable[[Path], ty.List[str]]],
        target: ty.Optional[Path] = None
    ) -> ty.Tuple[ty.Callable, ty.Callable]:
    '''
    Creates the functions a biome patch exposes.

    args:
    - source: biome source, a directory or a single .json file, relative to the
      'COMMON' root. A directory expands to its direct .json files.
    - step: index into the biome 'features' list, that is the generation step the
      feature ids are appended to.
    - features: the feature id(s) to append, or a callable receiving the output
      path of one biome and returning the feature ids for it.
    - target: output directory relative to the patch, defaults to
      '<patch_dir>/worldgen/biome'.

    returns:
    - (reference_file, process_multi), to be exposed by the patch module.
    '''
    def reference_file(patch_path: Path, patch_version_config: ty.Dict[str, str]):
        target_path = (patch_path.parent / 'worldgen' / 'biome') if target is None else (patch_path.parent / target)
        return ('COMMON', source, target_path)

    def process_multi(content: ty.List[ty.Tuple[Path, ty.Dict]]) -> ty.List[ty.Tuple[Path, ty.Dict]]:
        for target_path, biome_data in content:
            biome_features = features(target_path) if callable(features) else features
            if isinstance(biome_features, str):
                biome_features = [biome_features]
            biome_data['features'][step].extend(biome_features)
        return content

    return reference_file, process_multi
