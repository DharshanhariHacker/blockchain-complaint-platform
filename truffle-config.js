const HDWalletProvider = require('@truffle/hdwallet-provider');
const Web3 = require('web3');
const dotenv = require('dotenv');

dotenv.config();

const mnemonic = process.env.MNEMONIC;

module.exports = {
    networks: {
        development: {
            host: "127.0.0.1", // Use localhost
            port: 7545,        // Ganache GUI port
            network_id: "*",   // Any network (default: none)
        },
        ganache: {
            provider: () => new HDWalletProvider(mnemonic, `http://127.0.0.1:7545`),
            network_id: "*", // Match any network id
        },
    },
    compilers: {
        solc: {
            version: "0.8.27", // Specify the solc version
        },
    },
};
