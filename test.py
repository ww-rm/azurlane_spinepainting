from pathlib import Path
from typing import Dict, List, Optional

from pydantic import BaseModel, RootModel

ASSETS_DIR = Path("docs")


class Spine(BaseModel):
    skelName: str
    atlasName: str
    pages: List[str]


class Skin(BaseModel):
    chName: str
    spines: List[Spine]


class Ship(BaseModel):
    chName: str
    hxName: Optional[str] = None
    skins: Dict[str, Skin]


class ShipData(RootModel):
    root: Dict[str, Ship]


if __name__ == "__main__":
    shipdata = ShipData.model_validate_json(ASSETS_DIR.joinpath("index.json").read_bytes(), strict=True)

    nonexisted = []
    for shipname, ship in shipdata.root.items():
        shipd = ASSETS_DIR.joinpath(shipname)

        for skinname, skin in ship.skins.items():
            for spine in skin.spines:
                skelpath = shipd.joinpath(skinname, spine.skelName)
                if not skelpath.is_file():
                    nonexisted.append(skelpath)

                atlaspath = shipd.joinpath(skinname, spine.atlasName)
                if not atlaspath.is_file():
                    nonexisted.append(atlaspath)

                for page in spine.pages:
                    pagepath = shipd.joinpath(skinname, page)
                    if not pagepath.is_file():
                        nonexisted.append(pagepath)

    if len(nonexisted) > 0:
        raise FileNotFoundError(nonexisted)

    existed = []
    for shipd in ASSETS_DIR.iterdir():
        if not shipd.is_dir():
            continue

        shipname = shipd.name
        ship = shipdata.root.get(shipname)
        if ship is None:
            existed.append(shipd)
            continue

        for skind in shipd.iterdir():
            skinname = skind.name

            skin = ship.skins.get(skinname)
            if skin is None:
                existed.append(skind)
                continue

            valid_filenames = []
            valid_filenames.extend(sp.skelName for sp in skin.spines)
            valid_filenames.extend(sp.atlasName for sp in skin.spines)
            valid_filenames.extend(pagepath for sp in skin.spines for pagepath in sp.pages)

            for path in skind.iterdir():
                if path.name not in valid_filenames:
                    existed.append(path)

    if len(existed) > 0:
        raise FileExistsError(existed)
