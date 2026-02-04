---
name: jquery-ajax-json
description: Best practices for jQuery AJAX with JSON data handling including sending/receiving JSON, error handling, security (CSRF protection, XSS prevention), promise patterns, caching, and modern alternatives. Use when working with jQuery AJAX requests, implementing JSON APIs, troubleshooting AJAX issues, or migrating from jQuery to Fetch API.
---

# jQuery AJAX with JSON - Best Practices Skill

## Overview
Comprehensive guidance on using jQuery AJAX for sending and receiving JSON data with security, error handling, and modern best practices.

## Core jQuery AJAX Methods

### 1. $.ajax() - Complete Control

\`\`\`javascript
$.ajax({
    url: '/api/users',
    type: 'POST',
    dataType: 'json',
    contentType: 'application/json',
    data: JSON.stringify({ name: 'John', email: 'john@example.com' }),
    timeout: 10000,
    headers: { 'X-CSRF-Token': $('meta[name="csrf-token"]').attr('content') }
})
.done(function(response) { /* Handle success */ })
.fail(function(xhr) { /* Handle error */ })
.always(function() { /* Cleanup */ });
\`\`\`

### 2. $.getJSON() - GET Shorthand

\`\`\`javascript
$.getJSON('/api/users', { active: true })
    .done(function(data) { console.log(data); })
    .fail(function(xhr) { console.error(xhr); });
\`\`\`

## Critical Best Practices

### 1. Always Use JSON.stringify() for Complex Data

❌ **Bad:**
\`\`\`javascript
$.ajax({
    url: '/api/users',
    type: 'POST',
    data: { name: 'John', preferences: { theme: 'dark' } }
    // jQuery serializes as form data, not JSON!
});
\`\`\`

✅ **Good:**
\`\`\`javascript
$.ajax({
    url: '/api/users',
    type: 'POST',
    contentType: 'application/json',
    data: JSON.stringify({ name: 'John', preferences: { theme: 'dark' } })
});
\`\`\`

### 2. Comprehensive Error Handling

\`\`\`javascript
$.ajax({ url: '/api/users' })
.done(function(data) { handleSuccess(data); })
.fail(function(xhr, textStatus, errorThrown) {
    let errorMessage = 'An error occurred';
    
    if (xhr.status === 400) errorMessage = 'Invalid request';
    else if (xhr.status === 401) { 
        errorMessage = 'Unauthorized';
        window.location.href = '/login';
    }
    else if (xhr.status === 500) errorMessage = 'Server error';
    else if (textStatus === 'timeout') errorMessage = 'Request timed out';
    
    showErrorMessage(errorMessage);
});
\`\`\`

### 3. Security - CSRF Token Protection

\`\`\`javascript
// Global setup
$(document).ready(function() {
    const csrfToken = $('meta[name="csrf-token"]').attr('content');
    $.ajaxSetup({ headers: { 'X-CSRF-Token': csrfToken } });
});
\`\`\`

### 4. Input Validation

\`\`\`javascript
function createUser() {
    const userData = {
        name: $('#name').val().trim(),
        email: $('#email').val().trim()
    };
    
    const errors = [];
    if (!userData.name || userData.name.length < 2) 
        errors.push('Name must be at least 2 characters');
    if (!isValidEmail(userData.email)) 
        errors.push('Invalid email');
    
    if (errors.length > 0) {
        showErrors(errors);
        return;
    }
    
    $.ajax({
        url: '/api/users',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(userData)
    });
}
\`\`\`

### 5. Promise-Based API Service Layer

\`\`\`javascript
const UserAPI = {
    getAll: (filters) => $.ajax({ url: '/api/users', data: filters }),
    getById: (id) => $.ajax({ url: \`/api/users/\${id}\` }),
    create: (data) => $.ajax({
        url: '/api/users',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data)
    }),
    update: (id, data) => $.ajax({
        url: \`/api/users/\${id}\`,
        type: 'PUT',
        contentType: 'application/json',
        data: JSON.stringify(data)
    })
};
\`\`\`

## Advanced Patterns

### Request Cancellation

\`\`\`javascript
let currentRequest = null;

function searchUsers(query) {
    if (currentRequest) currentRequest.abort();
    
    currentRequest = $.ajax({
        url: '/api/users/search',
        data: { q: query },
        timeout: 5000
    }).always(() => currentRequest = null);
}
\`\`\`

### Response Caching

\`\`\`javascript
const cache = {};
function getCachedData(url) {
    if (cache[url]) return $.Deferred().resolve(cache[url]);
    return $.ajax({ url }).done(data => cache[url] = data);
}
\`\`\`

### Batch Requests

\`\`\`javascript
Promise.all([
    $.getJSON('/api/stats'),
    $.getJSON('/api/orders'),
    $.getJSON('/api/revenue')
]).then(([stats, orders, revenue]) => {
    displayStats(stats);
    displayOrders(orders);
    displayRevenue(revenue);
});
\`\`\`

## Security Checklist

- [ ] CSRF token included in state-changing requests
- [ ] HTTPS used for sensitive data
- [ ] User input escaped before display (use .text() not .html())
- [ ] Input validation on client and server
- [ ] Error messages don't expose sensitive info
- [ ] Rate limiting implemented

## Common Pitfalls to Avoid

1. ❌ Not setting contentType: 'application/json'
2. ❌ No error handling (.fail)
3. ❌ Using synchronous requests (async: false)
4. ❌ Multiple enumerations of data
5. ❌ Not cleaning up event handlers

## Modern Alternative: Fetch API

\`\`\`javascript
async function createUser(userData) {
    try {
        const response = await fetch('/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRF-Token': document.querySelector('[name=csrf-token]').content
            },
            body: JSON.stringify(userData)
        });
        
        if (!response.ok) throw new Error('Request failed');
        return await response.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
}
\`\`\`
