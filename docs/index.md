# Graph Auth

```graphql

query Me {
  me {
    id
    email
    username
    dateJoined
    lastLogin
    status {
      id
      verified
      archived
    }
    firstName
    lastName
    isActive
    isStaff
    isSuperuser
  }
}

query GetUserStatus {
  userstatus(verified: false) {
    edges {
      node {
        id
        verified
        archived
        user {
          id
          email
          username
          dateJoined
        }
      }
    }
  }
}


query GetUser {
  user(id: "1") {
    id
    email
    username
    dateJoined
    status {
      id
      verified
      archived
    }
  }
}

mutation RegisterUser {
  register(
    email: "demo2@traleor.com"
    username: "demo2"
    password: "supersecretpassword"
  ) {
    success
    errors
    user {
      id
      email
      username
      status {
        id
        verified
        archived
      }
    }
  }
}

mutation VerifyAccount {
  verifyAccount(
    token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjc3NzIxNjgzLCJvcmlnSWF0IjoxNjc3NzIxMzgzfQ.Xf23ObOucF8D-pNewqF5UekkxnOsMxA_6HxaCiKmt10"
  ) {
    success
    errors
  }
}

mutation ResendActivationEmail {
  resendActivationEmail(email: "demo1@traleor.com") {
    errors
    success
  }
}

mutation SendPasswordReset {
  sendPasswordResetEmail(email: "demo1@traleor.com") {
    errors
    success
  }
}

mutation Verify {
  verifyToken(
    token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjc3NzIxNjgzLCJvcmlnSWF0IjoxNjc3NzIxMzgzfQ.Xf23ObOucF8D-pNewqF5UekkxnOsMxA_6HxaCiKmt10"
  ) {
    payload
  }
}

mutation PasswordReset {
  passwordReset(
    token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNjc3NzIxNjgzLCJvcmlnSWF0IjoxNjc3NzIxMzgzfQ.Xf23ObOucF8D-pNewqF5UekkxnOsMxA_6HxaCiKmt10"
    newPassword: "password"
  ) {
    errors
    success
  }
}

mutation Login {
  tokenAuth(username: "admin", password: "password") {
    token
    payload
    refreshExpiresIn
  }
}

mutation Logout {
  deleteTokenCookie {
    deleted
  }
}

```