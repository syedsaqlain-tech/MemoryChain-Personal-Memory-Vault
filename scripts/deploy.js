const { ethers } = require("hardhat");

async function main() {
    console.log("Deploying MemoryChain...");

    const MemoryChain = await ethers.getContractFactory("MemoryChain");

    const memoryChain = await MemoryChain.deploy();

    await memoryChain.deployed();

    console.log("Contract deployed to:", memoryChain.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });