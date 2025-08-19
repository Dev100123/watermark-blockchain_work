// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProductTracker {
    struct Product {
        string hash_code;
        string name_registration;
        bool exists;
    }

    mapping(string => Product) public products;
    string[] public productIds;

    function addOrUpdateProduct(
        string memory hash_code,
        string memory name_registration
    ) public {
        if (!products[hash_code].exists) {
            productIds.push(hash_code);
        }

        products[hash_code] = Product(
            hash_code, name_registration, true
        );
    }

    function getProduct(string memory hash_code) public view returns (
        string memory, string memory
    ) {
        Product memory p = products[hash_code];
        require(p.exists, "Product does not exist");
        return (
            p.hash_code, p.name_registration
        );
    }

    function getProductCount() public view returns (uint) {
        return productIds.length;
    }

    function getProductByIndex(uint index) public view returns (
        string memory, string memory
    ) {
        string memory hash_code = productIds[index];
        return getProduct(hash_code);
    }
}
