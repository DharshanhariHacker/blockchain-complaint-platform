const ComplaintPlatform = artifacts.require("ComplaintPlatform");

contract("ComplaintPlatform", (accounts) => {
    it("should submit a complaint", async () => {
        const instance = await ComplaintPlatform.deployed();
        await instance.submitComplaint("encrypted data");
        const complaint = await instance.getComplaint(0);
        assert.equal(complaint[0], "encrypted data", "The complaint data should match");
    });

    it("should update the status", async () => {
        const instance = await ComplaintPlatform.deployed();
        await instance.updateStatus(0, "Resolved");
        const complaint = await instance.getComplaint(0);
        assert.equal(complaint[1], "Resolved", "The complaint status should be updated");
    });
});
