@IsTest
private class JiraCommentControllerTest {

    @TestSetup
    static void makeData() {
        insert new List<Case>{
            new Case(Subject = 'Jira Test Case', Jira_Number__c = 'TEST-100'),
            new Case(Subject = 'Blocked Jira Case', Block_Jira_Updates__c = 'Yes')
        };
    }

    private static void setRequest(String body) {
        RestContext.request = new RestRequest();
        RestContext.response = new RestResponse();
        RestContext.request.requestURI = '/services/apexrest/jira/comment';
        RestContext.request.httpMethod = 'POST';
        RestContext.request.requestBody = Blob.valueOf(body);
    }

    @IsTest
    static void testSuccessWithCaseId() {
        Case c = [SELECT Id FROM Case WHERE Subject = 'Jira Test Case' LIMIT 1];

        setRequest(JSON.serialize(new Map<String, String>{
            'caseId' => c.Id,
            'jiraIssueKey' => 'TEST-100',
            'commentBody' => 'This is a Jira comment',
            'authorName' => 'Jane Engineer',
            'commentTimestamp' => '2026-06-02T12:00:00Z'
        }));

        Test.startTest();
        JiraCommentController.handleComment();
        Test.stopTest();

        System.assertEquals(200, RestContext.response.statusCode, 'Expected 200 OK');
        Map<String, Object> resp = (Map<String, Object>) JSON.deserializeUntyped(
            RestContext.response.responseBody.toString()
        );
        System.assertEquals('success', resp.get('status'));
        System.assertNotEquals(null, resp.get('commentId'));

        List<CaseComment> comments = [SELECT CommentBody FROM CaseComment WHERE ParentId = :c.Id];
        System.assertEquals(1, comments.size(), 'Expected one CaseComment created');
        System.assert(comments[0].CommentBody.contains('Jane Engineer'), 'Comment body should include author name');

        Case updated = [SELECT Last_Jira_Comment_Date_Time__c FROM Case WHERE Id = :c.Id];
        System.assertNotEquals(null, updated.Last_Jira_Comment_Date_Time__c, 'DateTime field should be stamped');
    }

    @IsTest
    static void testSuccessWithJiraIssueKey() {
        setRequest(JSON.serialize(new Map<String, String>{
            'jiraIssueKey' => 'TEST-100',
            'commentBody' => 'Issue resolved by engineering',
            'authorName' => 'Dev User'
        }));

        Test.startTest();
        JiraCommentController.handleComment();
        Test.stopTest();

        System.assertEquals(200, RestContext.response.statusCode);
        Case c = [SELECT Id FROM Case WHERE Jira_Number__c = 'TEST-100' LIMIT 1];
        System.assertEquals(1, [SELECT Id FROM CaseComment WHERE ParentId = :c.Id].size());
    }

    @IsTest
    static void testBlockedCase() {
        Case c = [SELECT Id FROM Case WHERE Subject = 'Blocked Jira Case' LIMIT 1];

        setRequest(JSON.serialize(new Map<String, String>{
            'caseId' => c.Id,
            'commentBody' => 'This should be blocked',
            'authorName' => 'Someone'
        }));

        Test.startTest();
        JiraCommentController.handleComment();
        Test.stopTest();

        System.assertEquals(200, RestContext.response.statusCode);
        Map<String, Object> resp = (Map<String, Object>) JSON.deserializeUntyped(
            RestContext.response.responseBody.toString()
        );
        System.assertEquals('blocked', resp.get('status'));
        System.assertEquals(0, [SELECT Id FROM CaseComment WHERE ParentId = :c.Id].size(),
            'No CaseComment should be created for a blocked case');
    }

    @IsTest
    static void testCaseNotFound() {
        setRequest(JSON.serialize(new Map<String, String>{
            'jiraIssueKey' => 'NONEXISTENT-999',
            'commentBody' => 'Comment for a case that does not exist'
        }));

        Test.startTest();
        JiraCommentController.handleComment();
        Test.stopTest();

        System.assertEquals(404, RestContext.response.statusCode);
    }

    @IsTest
    static void testMissingIdentifier() {
        setRequest(JSON.serialize(new Map<String, String>{
            'commentBody' => 'No caseId or jiraIssueKey provided'
        }));

        Test.startTest();
        JiraCommentController.handleComment();
        Test.stopTest();

        System.assertEquals(400, RestContext.response.statusCode);
    }

    @IsTest
    static void testBuildCommentBody_withAllFields() {
        JiraCommentController.JiraCommentRequest req = new JiraCommentController.JiraCommentRequest();
        req.authorName = 'Test Author';
        req.jiraIssueKey = 'PROJ-42';
        req.commentBody = 'Fixed in latest build';

        String result = JiraCommentController.buildCommentBody(req);
        System.assert(result.contains('Test Author'), 'Should include author name');
        System.assert(result.contains('PROJ-42'), 'Should include Jira issue key');
        System.assert(result.contains('Fixed in latest build'), 'Should include comment body');
    }

    @IsTest
    static void testBuildCommentBody_missingOptionalFields() {
        JiraCommentController.JiraCommentRequest req = new JiraCommentController.JiraCommentRequest();

        String result = JiraCommentController.buildCommentBody(req);
        System.assert(result.contains('Unknown'), 'Should default author to Unknown');
        System.assert(result.contains('(no comment body)'), 'Should show placeholder for empty body');
    }
}
