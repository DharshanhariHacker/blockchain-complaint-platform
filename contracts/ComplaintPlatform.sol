// SPDX-License-Identifier: MIT
pragma solidity 0.8.19;

contract ComplaintPlatform {
    struct Complaint {
        address complainant;
        string encryptedData;
        string status;
    }

    Complaint[] public complaints;

    event ComplaintSubmitted(uint complaintId, address complainant);
    event StatusUpdated(uint complaintId, string newStatus);

    function submitComplaint(string memory encryptedData) public {
        complaints.push(Complaint(msg.sender, encryptedData, "Submitted"));
        emit ComplaintSubmitted(complaints.length - 1, msg.sender);
    }

    function updateStatus(uint complaintId, string memory newStatus) public {
        complaints[complaintId].status = newStatus;
        emit StatusUpdated(complaintId, newStatus);
    }

    function getComplaint(uint complaintId) public view returns (string memory, string memory) {
        return (complaints[complaintId].encryptedData, complaints[complaintId].status);
    }

    function totalComplaints() public view returns (uint) {
        return complaints.length;
    }
}
