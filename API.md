Supposed flow of the API - see request body for these requests in /docs/

- Auth
  - 1. userSignupRequest  -- POST /users - sign urself up
  - 2. loginRequest -- POST /api-token-auth/ - get a token
  - 3. checkAuthorizationToken -- POSt /api-token-verify/ - check if ur good to go
  - 4. renewAuthorizationToken -- POST /api-token-refresh/ - if u want a new token

- Account
  - 5. addNewPlant -- POST /plants/

- Plant
  - 6. fetchPlants -- GET /plants/

- Account
  - 7. updatePlant -- PUT /plants/{plant_id}
  - 8. deletePlant -- DELETE /plants/{plant_id}

- Cart
  - 9. updatedQuantity -- PUT /plants/{plant_id}
  - 10. placeOrder -- POST /orders/

- Account
  - 11. fetchOrders -- GET /orders/ 
