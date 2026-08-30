# Use-Case Flow: Cancel Subscription

**Use Case Name:** Cancel Subscription
**Primary Actor:** Individual User
**Preconditions:** 
- The user is logged into the app.
- The user has imported their bank transactions.
- The system has identified at least one active subscription.
**Postconditions:** 
- The subscription is marked as "Cancelled" in the system.
- The user's monthly burn rate is recalculated and updated.

### Main Success Scenario:
1. The **User** selects a specific subscription from their active subscriptions list on the Dashboard.
2. The **User** clicks the "Cancel Subscription" button.
3. The **System** searches its database and displays the specific "Cancellation Guide" or direct cancellation link for that service.
4. The **User** follows the guide to cancel the service externally, then returns to the app and clicks "Mark as Cancelled".
5. The **System** updates the subscription status to "Cancelled" in the database.
6. The **System** recalculates the monthly burn rate (subtracting the cancelled cost).
7. The **System** displays a success message and shows the updated burn rate.

### Alternate Flow:
**3a. Cancellation Guide Not Found**
1. The **System** cannot find a specific cancellation guide or link for the selected service in its database.
2. The **System** displays a generic message: *"We don't have a guide for this service yet. Please visit their website to cancel."* and provides a link to a Google search for the service name.
3. The **User** figures out how to cancel it externally, returns to the app, and clicks "Mark as Cancelled".
4. *Return to Step 5 of the Main Success Scenario.*
