# Xavier Project

> Everyone, everywhere, all at once

Xavier is a comprehensive system designed to gather, process, and provide detailed information about professors and researchers worldwide, including their affiliations, research interests, and publications.

## Project Overview

The Xavier project is divided into three main components:

1. **Xavier Telepath**: Responsible for data scraping and gathering from various sources.
2. **Xavier Mind**: Handles data cleaning and profile generation.
3. **Xavier Oracle**: Manages API responses and AI-driven interactions.

<details>
<summary>Xavier Telepath</summary>

The Telepath component focuses on collecting raw data from various sources, including:

- Academic websites
- Publication databases
- Social media platforms
- Public APIs

</details>

### Xavier Mind

The Mind component processes the raw data collected by Telepath:

- Cleans and normalizes the data
- Generates comprehensive profiles for researchers and their publications
- Integrates data into a knowledge graph for advanced querying

### Xavier Oracle

The Oracle component serves as the interface for users to interact with the processed data:

- Provides RESTful APIs for data retrieval
- Implements AI-driven query processing and response generation
- Offers recommendations based on the integrated data

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/thisismeamir/xavier.git
   cd xavier
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To use the Xavier project:

1. Set up the environment variables:
   ```
   cp .env.example .env
   ```
   Edit the `.env` file with your specific configurations.

2. Run Xavier Telepath to gather data:
   ```
   python -m xavier_telepath
   ```

3. Process the gathered data with Xavier Mind:
   ```
   python -m xavier_mind
   ```

4. Start the Xavier Oracle API server:
   ```
   python -m xavier_oracle
   ```

For more detailed usage instructions, please refer to the documentation in each component's directory.

## Contributing

We welcome contributions to the Xavier project! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please make sure to update tests as appropriate and adhere to the project's coding standards.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Contact

Project Maintainer: Kid A
- Email: thisismeamir@outlook.com
- Telegram: @thisismeamir

Xavier Project Telegram Channel: [Xavier Channel](https://t.me/+5qEkHVO-6V9iNjI8)

## Show Your Support

If you find this project useful, please consider giving it a star on GitHub! Your support helps to increase the visibility of the project and encourages further development.

## Donations

If you'd like to support the development of Xavier, consider making a donation. Your contributions help maintain the project and fund new features.
Thank you for your support!

BTC: 
bc1qc7x6jum26ppkgj709lxwaepx8cy8agu3hz4yam

USDT Etherium:
0xD9FC2B0e34e3D15AafA5C9d6aD121F97a95d1E6c
