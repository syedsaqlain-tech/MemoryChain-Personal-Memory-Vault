// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract MemoryChain {

    struct Memory {
        string title;
        string description;
        string fileHash;
    }

    Memory[] public memories;

    function addMemory(
        string memory _title,
        string memory _description,
        string memory _fileHash
    ) public {
        memories.push(Memory(_title, _description, _fileHash));
    }

    function getMemory(uint index)
        public
        view
        returns (
            string memory,
            string memory,
            string memory
        )
    {
        Memory memory m = memories[index];
        return (m.title, m.description, m.fileHash);
    }

    function totalMemories() public view returns (uint) {
        return memories.length;
    }
}