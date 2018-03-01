# dozendigits

> A Multiplication Tester

## Build Setup

1. Load the [CloudFormation Template](cloudformation.json) into your aws account.
2. Fill in whatever parameters you wish for your bucketname and DynamoDB table name (as long as they're available)
3. Create the Stack
4. Wait a bit (maybe as much as 5 minutes)
5. Visit the 'Outputs' tab to see the URL of your new Multiplication Tester Website.

## To make it your own

I initialized the front end using [this Vue repo](https://github.com/vuejs-templates/webpack-simple). Visit its documentation for more info.
When you've got it ready, just `npm run build` and copy the `dist` folder to your newly created s3 bucket.

You've also got some shiny new Lambda functions that you can mess around with. If you're looking for a place to start, you can modify how [DozenDigitsGetQuestion](lambda/DozenDigitsGetQuestion.py) determines what is an "easy" question and what's a "hard" one. It'd be great to base it on your user's past performance.
