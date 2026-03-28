# HabitHush: The Distraction Blocker

HabitHush is a CLI tool designed to boost productivity by temporarily modifying the local hosts file to block distracting websites. Users can define lists of 'distraction' domains and toggle them on or off using simple commands like 'habit-hush block' or 'habit-hush allow'. It includes a timer feature that automatically lifts the block after a specified number of minutes, helping users maintain focus sessions. The tool manages state using a simple JSON configuration file, ensuring cross-session persistence without needing a database. It is perfect for developers who need to discipline their browsing habits while staying within the terminal environment.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Modules](#modules)
- [Future Work](#future-work)
- [License](#license)

## Installation

```bash
git clone <repo-url>
cd habithush:-the-distraction-blocker
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

Run the main entry point to start HabitHush: The Distraction Blocker.

## Project Structure

```
├── cli.py
├── engine.py
├── hosts_manager.py
├── config_handler.py
├── timer.py
├── requirements.txt
└── README.md
```

## Modules

- **entry_point**: Core module for entry_point functionality.
- **core**: Core module for core functionality.
- **system**: Core module for system functionality.
- **utils**: Core module for utils functionality.

## Future Work

- [ ] Add comprehensive test suite
- [ ] Implement CI/CD pipeline
- [ ] Add Docker support
- [ ] Improve error handling and edge cases
- [ ] Add configuration documentation
- [ ] Performance optimization

## License

This project is licensed under the MIT License.
