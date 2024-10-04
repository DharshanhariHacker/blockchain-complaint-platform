const Web3 = require("web3");
const ComplaintPlatform = artifacts.require("ComplaintPlatform");

module.exports = async function (deployer) {
    await deployer.deploy(ComplaintPlatform);
    console.log("ComplaintPlatform deployed at:", ComplaintPlatform.address);
};
