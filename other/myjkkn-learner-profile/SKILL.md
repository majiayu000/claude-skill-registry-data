---
name: myjkkn-learner-profile
description: Pattern for fetching learner profiles from MyJKKN API with pagination support. Use when needing to retrieve learner photo URLs, DOB, or other profile data from MyJKKN. Handles the 200-record-per-page API limitation through pagination and uses myjkkn_institution_ids from COE institution table for filtering.
---

# MyJKKN Learner Profile Fetching

Pattern for retrieving learner profiles from MyJKKN API with proper institution filtering and pagination.

## Key Constraints

1. **API Pagination**: MyJKKN API returns max 200 records per page regardless of `limit` parameter
2. **Institution Filtering**: Use `myjkkn_institution_ids` array from COE `institutions` table
3. **Matching Field**: Match profiles by `register_number` only (not roll_number)
4. **Server-side filtering unreliable**: Always filter by `institution_id` client-side after fetching

## Environment Variables

```typescript
const myjkknApiUrl = process.env.MYJKKN_API_URL  // e.g., https://jkkn.ai
const myjkknApiKey = process.env.MYJKKN_API_KEY
```

## Implementation Pattern

### Step 1: Get myjkkn_institution_ids from COE Institution

```typescript
const { data: institution } = await supabase
  .from('institutions')
  .select('myjkkn_institution_ids')
  .eq('institution_code', institutionCode)
  .single()

const myjkknInstIds: string[] = institution?.myjkkn_institution_ids || []
```

### Step 2: Fetch Profiles with Pagination

Loop through each MyJKKN institution ID and paginate through all profiles:

```typescript
let matchingProfile: any = null

for (const myjkknInstId of myjkknInstIds) {
  if (matchingProfile) break  // Stop if we found a match

  let page = 1
  const pageSize = 200
  let hasMorePages = true

  while (hasMorePages && !matchingProfile) {
    const profileParams = new URLSearchParams()
    profileParams.set('institution_id', myjkknInstId)
    profileParams.set('limit', String(pageSize))
    profileParams.set('page', String(page))

    const profileResponse = await fetch(
      `${myjkknApiUrl}/api-management/learners/profiles?${profileParams.toString()}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${myjkknApiKey}`,
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        },
        cache: 'no-store',
      }
    )

    if (profileResponse.ok) {
      const profileData = await profileResponse.json()
      const profiles = profileData.data || []

      // Find matching profile by register_number only
      matchingProfile = profiles.find((p: any) =>
        p.register_number === targetRegisterNumber
      )

      // Check if there are more pages
      hasMorePages = profiles.length === pageSize
      page++
    } else {
      hasMorePages = false
    }
  }
}
```

### Step 3: Extract Profile Data

Photo URL fields to check (in order of preference):

```typescript
const photoUrl = matchingProfile?.student_photo_url
  || matchingProfile?.photo_url
  || matchingProfile?.profile_photo
  || matchingProfile?.image_url
  || null

const dob = matchingProfile?.date_of_birth || null
```

## Complete Example

```typescript
async function fetchLearnerProfile(
  supabase: SupabaseClient,
  institutionCode: string,
  registerNumber: string
): Promise<{ photoUrl: string | null; dob: string | null }> {
  const myjkknApiUrl = process.env.MYJKKN_API_URL
  const myjkknApiKey = process.env.MYJKKN_API_KEY

  if (!myjkknApiKey || !myjkknApiUrl) {
    return { photoUrl: null, dob: null }
  }

  // Get myjkkn_institution_ids from COE institution
  const { data: institution } = await supabase
    .from('institutions')
    .select('myjkkn_institution_ids')
    .eq('institution_code', institutionCode)
    .single()

  const myjkknInstIds: string[] = institution?.myjkkn_institution_ids || []

  if (myjkknInstIds.length === 0) {
    return { photoUrl: null, dob: null }
  }

  let matchingProfile: any = null

  for (const myjkknInstId of myjkknInstIds) {
    if (matchingProfile) break

    let page = 1
    const pageSize = 200
    let hasMorePages = true

    while (hasMorePages && !matchingProfile) {
      const profileParams = new URLSearchParams()
      profileParams.set('institution_id', myjkknInstId)
      profileParams.set('limit', String(pageSize))
      profileParams.set('page', String(page))

      try {
        const profileResponse = await fetch(
          `${myjkknApiUrl}/api-management/learners/profiles?${profileParams.toString()}`,
          {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${myjkknApiKey}`,
              'Accept': 'application/json',
              'Content-Type': 'application/json',
            },
            cache: 'no-store',
          }
        )

        if (profileResponse.ok) {
          const profileData = await profileResponse.json()
          const profiles = profileData.data || []

          matchingProfile = profiles.find((p: any) =>
            p.register_number === registerNumber
          )

          hasMorePages = profiles.length === pageSize
          page++
        } else {
          hasMorePages = false
        }
      } catch (error) {
        console.error('MyJKKN API error:', error)
        hasMorePages = false
      }
    }
  }

  if (!matchingProfile) {
    return { photoUrl: null, dob: null }
  }

  const photoUrl = matchingProfile.student_photo_url
    || matchingProfile.photo_url
    || matchingProfile.profile_photo
    || matchingProfile.image_url
    || null

  const dob = matchingProfile.date_of_birth || null

  return { photoUrl, dob }
}
```

## Batch Fetching Pattern

For batch operations (multiple learners), fetch all profiles first, then match:

```typescript
const allProfiles: any[] = []

for (const myjkknInstId of myjkknInstIds) {
  let page = 1
  const pageSize = 200
  let hasMorePages = true

  while (hasMorePages) {
    const profileParams = new URLSearchParams()
    profileParams.set('institution_id', myjkknInstId)
    profileParams.set('limit', String(pageSize))
    profileParams.set('page', String(page))

    const response = await fetch(
      `${myjkknApiUrl}/api-management/learners/profiles?${profileParams.toString()}`,
      {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${myjkknApiKey}`,
          'Accept': 'application/json',
        },
        cache: 'no-store',
      }
    )

    if (response.ok) {
      const data = await response.json()
      const profiles = data.data || []
      allProfiles.push(...profiles)
      hasMorePages = profiles.length === pageSize
      page++
    } else {
      hasMorePages = false
    }
  }
}

// Create lookup map by register_number
const profileMap = new Map(
  allProfiles.map(p => [p.register_number, p])
)

// Use map for O(1) lookup
const profile = profileMap.get(registerNumber)
```

## API Endpoint Reference

- **Endpoint**: `GET /api-management/learners/profiles`
- **Auth**: Bearer token in Authorization header
- **Query Params**:
  - `institution_id`: MyJKKN institution UUID (required for filtering)
  - `limit`: Page size (max 200 enforced by API)
  - `page`: Page number (1-based)
- **Response**: `{ data: Profile[] }` or direct array
