// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SECOPS {
    mapping (address => bool) public unlockedUsers;

    function unlock(bytes32 _key) public {
        require(_key == 0x7365636f70735f707269766174655f6b65790000000000000000000000000000, "That not the key !");
        unlockedUsers[msg.sender] = true;
    }
    
    function getFlag()external view returns(bytes32){
        require(unlockedUsers[msg.sender] == true, "It is still locked for you !");
        bytes32 enc_flag = 0x23372a3931271e0858291a6f04400002552d1b13572c04276834316e7d000000;
        bytes32 key = 0x707269766174655f6b65795f69735f766572795f676f6f640000000000000000; 
        bytes32 flag = enc_flag^key;
        return flag;
    }

}