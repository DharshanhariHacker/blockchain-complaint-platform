const HDWalletProvider = require('@truffle/hdwallet-provider');
const dotenv = require('dotenv');
const path = require('path');

// Load .env from backend folder
dotenv.config({ path: path.resolve(__dirname, 'backend/.env') });

const mnemonic = process.env.MNEMONIC;

if (!mnemonic) {
  throw new Error("Mnemonic is not defined in the .env file");
}

module.exports = {
  networks: {
    development: {
      provider: () => new HDWalletProvider({
        mnemonic: {
          phrase: mnemonic
        },
        providerOrUrl: "http://127.0.0.1:7545", // Local Ganache URL
      }),
      network_id: "*", // Match any network id
    },
  },
  compilers: {
    solc: {
      version: "0.8.19", // Specify solc version
    }
  },
};
