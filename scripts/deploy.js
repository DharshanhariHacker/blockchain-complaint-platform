var Web3 = require("web3");
var ComplaintPlatform = artifacts.require("ComplaintPlatform");

module.exports = async function (deployer) {
    await deployer.deploy(ComplaintPlatform);
    console.log("ComplaintPlatform deployed at:", ComplaintPlatform.address);
};
