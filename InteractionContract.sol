// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InteractionContract {
    struct Interaction {
        uint256 requestId;
        string consumerName;
        uint256 allocatedResources;
        uint256 usedResources;
        uint256 unusedResources; // New field for storing unused resources
    }

    event InteractionData(
        uint256 indexed requestId,
        string consumerName,
        uint256 allocatedResources,
        uint256 usedResources,
        uint256 unusedResources // Updated event signature
    );

    mapping(uint256 => Interaction) public interactions;
    uint256 public interactionCount;

    function storeInteraction(
        uint256 _requestId,
        string memory _consumerName,
        uint256 _allocatedResources,
        uint256 _usedResources,
        uint256 _unusedResources // Updated function parameter
    ) public {
        Interaction storage newInteraction = interactions[_requestId];
        newInteraction.requestId = _requestId;
        newInteraction.consumerName = _consumerName;
        newInteraction.allocatedResources = _allocatedResources;
        newInteraction.usedResources = _usedResources;
        newInteraction.unusedResources = _unusedResources; // Store the unused resources

        emit InteractionData(_requestId, _consumerName, _allocatedResources, _usedResources, _unusedResources);

        interactionCount++;
    }
}
