@RestResource(urlMapping='/jira/comment')
global without sharing class JiraCommentController {

    global class JiraCommentRequest {
        global String caseId;
        global String jiraIssueKey;
        global String commentBody;
        global String authorName;
        global String commentTimestamp;
    }

    global class JiraCommentResponse {
        global String status;
        global String message;
        global String commentId;

        global JiraCommentResponse(String statusVal, String messageVal) {
            this.status = statusVal;
            this.message = messageVal;
        }
    }

    @HttpPost
    global static void handleComment() {
        RestRequest req = RestContext.request;
        RestResponse res = RestContext.response;
        res.addHeader('Content-Type', 'application/json');

        try {
            JiraCommentRequest payload = (JiraCommentRequest) JSON.deserialize(
                req.requestBody.toString(),
                JiraCommentRequest.class
            );

            if (String.isBlank(payload.caseId) && String.isBlank(payload.jiraIssueKey)) {
                res.statusCode = 400;
                res.responseBody = Blob.valueOf(JSON.serialize(
                    new JiraCommentResponse('error', 'caseId or jiraIssueKey is required')
                ));
                return;
            }

            List<Case> cases;
            if (String.isNotBlank(payload.caseId)) {
                cases = [
                    SELECT Id, OwnerId, Block_Jira_Updates__c
                    FROM Case
                    WHERE Id = :payload.caseId
                    LIMIT 1
                ];
            } else {
                cases = [
                    SELECT Id, OwnerId, Block_Jira_Updates__c
                    FROM Case
                    WHERE Jira_Number__c = :payload.jiraIssueKey
                    LIMIT 1
                ];
            }

            if (cases.isEmpty()) {
                res.statusCode = 404;
                res.responseBody = Blob.valueOf(JSON.serialize(
                    new JiraCommentResponse('error', 'No case found for the provided identifier')
                ));
                return;
            }

            Case c = cases[0];

            if (c.Block_Jira_Updates__c == 'Yes') {
                res.statusCode = 200;
                res.responseBody = Blob.valueOf(JSON.serialize(
                    new JiraCommentResponse('blocked', 'Jira updates are blocked for this case')
                ));
                return;
            }

            CaseComment comment = new CaseComment(
                ParentId = c.Id,
                CommentBody = buildCommentBody(payload),
                IsPublished = false
            );
            insert comment;

            c.Last_Jira_Comment_Date_Time__c = DateTime.now();
            update c;

            JiraCommentResponse successResponse = new JiraCommentResponse('success', 'Comment created successfully');
            successResponse.commentId = comment.Id;
            res.statusCode = 200;
            res.responseBody = Blob.valueOf(JSON.serialize(successResponse));

        } catch (Exception e) {
            res.statusCode = 500;
            res.responseBody = Blob.valueOf(JSON.serialize(
                new JiraCommentResponse('error', e.getMessage())
            ));
        }
    }

    @TestVisible
    private static String buildCommentBody(JiraCommentRequest payload) {
        String author = String.isNotBlank(payload.authorName) ? payload.authorName : 'Unknown';
        String issueRef = String.isNotBlank(payload.jiraIssueKey) ? ' (' + payload.jiraIssueKey + ')' : '';
        String body = String.isNotBlank(payload.commentBody) ? payload.commentBody : '(no comment body)';
        return '[Jira Comment from ' + author + issueRef + ']\n\n' + body;
    }
}
