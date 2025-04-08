import sys
import os
from recolor import Core

def main():
    if len(sys.argv) < 3:
        print("Usage: python run_examples.py <input_path> <output_folder>")
        return

    input_path = sys.argv[1]
    output_folder = sys.argv[2]

    os.makedirs(output_folder, exist_ok=True)

    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, 'simulate_protanopia.png'),
                  simulate_type='protanopia',
                  simulate_degree_primary=0.9)

    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, 'simulate_deutranopia.png'),
                  simulate_type='deutranopia',
                  simulate_degree_primary=0.9)

    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, 'simulate_tritanopia.png'),
                  simulate_type='tritanopia',
                  simulate_degree_primary=0.9)

    Core.simulate(input_path=input_path,
                  return_type='save',
                  save_path=os.path.join(output_folder, 'simulate_hybrid.png'),
                  simulate_type='hybrid',
                  simulate_degree_primary=0.5,
                  simulate_degree_sec=0.5)

    Core.correct(input_path=input_path,
                 return_type='save',
                 save_path=os.path.join(output_folder, 'corrected_protanopia.png'),
                 protanopia_degree=0.9,
                 deutranopia_degree=0.0)

    Core.simulate(input_path=os.path.join(output_folder, 'corrected_protanopia.png'),
                  return_type='save',
                  save_path=os.path.join(output_folder, 'simulate_corrected_protanopia.png'),
                  simulate_type='protanopia',
                  simulate_degree_primary=0.9)

    Core.correct(input_path=input_path,
                 return_type='save',
                 save_path=os.path.join(output_folder, 'corrected_deutranopia.png'),
                 protanopia_degree=0.0,
                 deutranopia_degree=1.0)

    Core.simulate(input_path=os.path.join(output_folder, 'corrected_deutranopia.png'),
                  return_type='save',
                  save_path=os.path.join(output_folder, 'simulate_corrected_deutranopia.png'),
                  simulate_type='deutranopia',
                  simulate_degree_primary=0.9)

    Core.correct(input_path=input_path,
                 return_type='save',
                 save_path=os.path.join(output_folder, 'corrected_hybrid.png'),
                 protanopia_degree=0.5,
                 deutranopia_degree=0.5)

if __name__ == '__main__':
    main()
