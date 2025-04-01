from ase.build import fcc111, molecule
from ase import Atom
import random
import sys

def create_slab(element):
    """
    Create an fcc111 surface slab for the specified element.
    """
    slab = fcc111(symbol=element, size=(10, 10, 4), vacuum=10.0)
    return slab

def add_gas(slab, gas, n):
    """
    Add the specified gas molecule/atom randomly on the slab.
    """
    cell = slab.get_cell()
    x_max = cell[0, 0]
    y_max = cell[1, 1]
    for _ in range(n):
        x = random.uniform(0, x_max)
        y = random.uniform(0, y_max)
        z = random.uniform(0, 5)
        try:
            mol = molecule(gas)
            alpha = random.uniform(0, 360)
            beta  = random.uniform(0, 360)
            gamma = random.uniform(0, 360)
            # Rotate molecule with random Euler angles
            mol.rotate(alpha, 'z', rotate_cell=False, center='COM')
            mol.rotate(beta,  'y', rotate_cell=False, center='COM')
            mol.rotate(gamma, 'x', rotate_cell=False, center='COM')
            # Translate molecule so its COM is at a random position
            com = mol.get_center_of_mass()
            mol.translate((x - com[0], y - com[1], z - com[2]))
            slab.extend(mol)
        except Exception:
            # If an error occurs with molecule() function, append as Atom.
            slab.append(Atom(gas, (x, y, z)))
    return slab

def make_fcc_surface_figure(slab_element, gas_element=None, gas_count=None, image_name=None):
    """
    Create an fcc111 slab for the specified element, optionally add gas molecules,
    and save an image. Returns the final slab.
    """
    slab = create_slab(slab_element)
    if gas_element and gas_count is not None:
        slab = add_gas(slab, gas_element, gas_count)
        if not image_name:
            image_name = f"{slab_element}_{gas_element}_{gas_count}.png"
    else:
        if not image_name:
            image_name = f"{slab_element}.png"
    
    # Remove adsorption info before saving the image.
    slab.info.pop("adsorbate_info", None)
    slab.write(image_name, rotation="100x")
    return slab

if __name__ == "__main__":
    if len(sys.argv) not in (2, 4):
        print("Usage: python make_fcc_surface_figure.py [slab_element] OR")
        print("       python make_fcc_surface_figure.py [slab_element] [gas_element] [gas_count]")
        sys.exit(1)
    
    slab_element = sys.argv[1]
    
    if len(sys.argv) == 4:
        gas_element = sys.argv[2]
        try:
            gas_count = int(sys.argv[3])
        except ValueError:
            print("gas_count must be an integer.")
            sys.exit(1)
        print(f"{slab_element} slab with {gas_count} {gas_element} molecules will be created.")
        image_name = f"{slab_element}_{gas_element}_{gas_count}.png"
        slab = make_fcc_surface_figure(slab_element, gas_element, gas_count, image_name)
    else:
        print(f"{slab_element} slab model will be created.")
        image_name = f"{slab_element}.png"
        slab = make_fcc_surface_figure(slab_element, image_name=image_name)
    
    print(f"Image saved as {image_name}")
