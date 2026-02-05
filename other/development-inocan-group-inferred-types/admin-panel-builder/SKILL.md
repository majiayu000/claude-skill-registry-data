---
name: admin-panel-builder
description: Expert assistant for creating and maintaining admin panel pages in the KR92 Bible Voice project. Use when creating admin pages, building admin components, integrating with admin navigation, or adding admin features.
---

# Admin Panel Builder

## Capabilities
- Scaffold admin page components with role checks
- Integrate with existing admin navigation
- Add proper table/form components using shadcn/ui
- Include RPC function calls and error handling
- Set up tabs and data management UI

## Admin Panel Structure

### Location
```
src/pages/Admin*.tsx
```

### Existing Admin Pages
- `AdminAIPage.tsx` - AI management (usage, prompts, features, pricing)
- `AdminAudioPage.tsx` - Audio/TTS management
- `AdminTopicsPage.tsx` - Topic management and translations
- `AdminUsersPage.tsx` - User and role management
- `AdminTranslationsPage.tsx` - Term translation cache
- `AdminVideoPage.tsx` - Video series and clips

## Usage Examples

### Example 1: Create New Admin Page
**User:** "Create an admin page for managing Bible versions"

**Assistant:**
```typescript
// src/pages/AdminVersionsPage.tsx

import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUserRole } from "@/hooks/useUserRole";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Loader2 } from "lucide-react";
import { VersionsList } from "@/components/admin/versions/VersionsList";
import { AddVersionForm } from "@/components/admin/versions/AddVersionForm";

const AdminVersionsPage = () => {
  const navigate = useNavigate();
  const { isAdmin, loading } = useUserRole();

  useEffect(() => {
    if (!loading && !isAdmin) {
      navigate("/");
    }
  }, [isAdmin, loading, navigate]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  if (!isAdmin) {
    return null;
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Bible Versions Management</h1>
        <p className="text-muted-foreground mt-2">
          Manage Bible translations and versions
        </p>
      </div>

      <Tabs defaultValue="versions" className="space-y-4">
        <TabsList>
          <TabsTrigger value="versions">Versions</TabsTrigger>
          <TabsTrigger value="add">Add Version</TabsTrigger>
          <TabsTrigger value="settings">Settings</TabsTrigger>
        </TabsList>

        <TabsContent value="versions" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Bible Versions</CardTitle>
              <CardDescription>
                List of all available Bible translations
              </CardDescription>
            </CardHeader>
            <CardContent>
              <VersionsList />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="add" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Add New Version</CardTitle>
              <CardDescription>
                Register a new Bible translation
              </CardDescription>
            </CardHeader>
            <CardContent>
              <AddVersionForm />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="settings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Version Settings</CardTitle>
              <CardDescription>
                Global settings for Bible versions
              </CardDescription>
            </CardHeader>
            <CardContent>
              {/* Settings content */}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default AdminVersionsPage;
```

### Example 2: Create Admin Component with Data Table
**User:** "Create component to list and manage Bible versions"

**Assistant:**
```typescript
// src/components/admin/versions/VersionsList.tsx

import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Loader2, Trash2, Edit, CheckCircle, XCircle } from "lucide-react";

export const VersionsList = () => {
  const { toast } = useToast();
  const queryClient = useQueryClient();
  const [deleteId, setDeleteId] = useState<string | null>(null);

  // Fetch versions
  const { data: versions, isLoading } = useQuery({
    queryKey: ['bible-versions'],
    queryFn: async () => {
      const { data, error } = await supabase
        .from('bible_versions')
        .select('*')
        .order('name');

      if (error) throw error;
      return data;
    },
  });

  // Delete mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: string) => {
      const { error } = await supabase
        .from('bible_versions')
        .delete()
        .eq('id', id);

      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bible-versions'] });
      toast({
        title: "Version deleted",
        description: "Bible version has been removed",
      });
      setDeleteId(null);
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  // Toggle active mutation
  const toggleActiveMutation = useMutation({
    mutationFn: async ({ id, is_active }: { id: string; is_active: boolean }) => {
      const { error } = await supabase
        .from('bible_versions')
        .update({ is_active: !is_active })
        .eq('id', id);

      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bible-versions'] });
      toast({
        title: "Status updated",
        description: "Version status has been changed",
      });
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  if (isLoading) {
    return (
      <div className="flex justify-center p-8">
        <Loader2 className="h-8 w-8 animate-spin" />
      </div>
    );
  }

  return (
    <>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Code</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>Language</TableHead>
            <TableHead>Status</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {versions?.map((version) => (
            <TableRow key={version.id}>
              <TableCell className="font-mono">{version.code}</TableCell>
              <TableCell>{version.name}</TableCell>
              <TableCell>{version.language}</TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => toggleActiveMutation.mutate({
                    id: version.id,
                    is_active: version.is_active
                  })}
                >
                  {version.is_active ? (
                    <Badge variant="default">
                      <CheckCircle className="h-3 w-3 mr-1" />
                      Active
                    </Badge>
                  ) : (
                    <Badge variant="secondary">
                      <XCircle className="h-3 w-3 mr-1" />
                      Inactive
                    </Badge>
                  )}
                </Button>
              </TableCell>
              <TableCell className="text-right space-x-2">
                <Button variant="outline" size="sm">
                  <Edit className="h-4 w-4" />
                </Button>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => setDeleteId(version.id)}
                >
                  <Trash2 className="h-4 w-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <AlertDialog open={!!deleteId} onOpenChange={() => setDeleteId(null)}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Delete Version</AlertDialogTitle>
            <AlertDialogDescription>
              Are you sure? This will permanently delete this Bible version.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => deleteId && deleteMutation.mutate(deleteId)}
            >
              Delete
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </>
  );
};
```

### Example 3: Create Form Component
**User:** "Create form to add new Bible version"

**Assistant:**
```typescript
// src/components/admin/versions/AddVersionForm.tsx

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { useToast } from "@/hooks/use-toast";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";

const formSchema = z.object({
  code: z.string().min(2).max(20),
  name: z.string().min(3),
  language: z.string().min(2),
  description: z.string().optional(),
  year: z.number().int().min(1000).max(2100).optional(),
  is_active: z.boolean().default(true),
});

type FormData = z.infer<typeof formSchema>;

export const AddVersionForm = () => {
  const { toast } = useToast();
  const queryClient = useQueryClient();

  const form = useForm<FormData>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      code: "",
      name: "",
      language: "fi",
      description: "",
      is_active: true,
    },
  });

  const addMutation = useMutation({
    mutationFn: async (values: FormData) => {
      const { error } = await supabase
        .from('bible_versions')
        .insert([values]);

      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['bible-versions'] });
      toast({
        title: "Version added",
        description: "New Bible version has been created",
      });
      form.reset();
    },
    onError: (error: Error) => {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    },
  });

  const onSubmit = (values: FormData) => {
    addMutation.mutate(values);
  };

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="code"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Version Code</FormLabel>
              <FormControl>
                <Input placeholder="finstlk201" {...field} />
              </FormControl>
              <FormDescription>
                Unique identifier (e.g., finstlk201, KJV)
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Version Name</FormLabel>
              <FormControl>
                <Input placeholder="Pyhä Raamattu (STLK 2017)" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="language"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Language</FormLabel>
              <Select onValueChange={field.onChange} defaultValue={field.value}>
                <FormControl>
                  <SelectTrigger>
                    <SelectValue placeholder="Select language" />
                  </SelectTrigger>
                </FormControl>
                <SelectContent>
                  <SelectItem value="fi">Finnish</SelectItem>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="sv">Swedish</SelectItem>
                </SelectContent>
              </Select>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description</FormLabel>
              <FormControl>
                <Textarea
                  placeholder="Brief description of this translation"
                  {...field}
                />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="is_active"
          render={({ field }) => (
            <FormItem className="flex items-center justify-between rounded-lg border p-4">
              <div className="space-y-0.5">
                <FormLabel className="text-base">Active</FormLabel>
                <FormDescription>
                  Make this version available to users
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
            </FormItem>
          )}
        />

        <Button type="submit" disabled={addMutation.isPending}>
          {addMutation.isPending ? "Adding..." : "Add Version"}
        </Button>
      </form>
    </Form>
  );
};
```

## Admin Page Checklist

### 1. Role Protection
```typescript
const { isAdmin, loading } = useUserRole();

useEffect(() => {
  if (!loading && !isAdmin) {
    navigate("/");
  }
}, [isAdmin, loading, navigate]);
```

### 2. Loading State
```typescript
if (loading) {
  return (
    <div className="flex items-center justify-center min-h-screen">
      <Loader2 className="h-8 w-8 animate-spin" />
    </div>
  );
}
```

### 3. Error Handling
```typescript
const { toast } = useToast();

// In mutation
onError: (error: Error) => {
  toast({
    title: "Error",
    description: error.message,
    variant: "destructive",
  });
}
```

### 4. Data Invalidation
```typescript
const queryClient = useQueryClient();

onSuccess: () => {
  queryClient.invalidateQueries({ queryKey: ['your-key'] });
}
```

## Common shadcn/ui Components

| Component | Use For |
|-----------|---------|
| `Card` | Section containers |
| `Tabs` | Multi-section pages |
| `Table` | Data lists |
| `Form` | Input forms |
| `Dialog` | Modals and confirmations |
| `AlertDialog` | Destructive actions |
| `Button` | Actions |
| `Badge` | Status indicators |
| `Select` | Dropdowns |
| `Switch` | Boolean toggles |

## Navigation Integration

Add to admin navigation (if needed):
```typescript
// In main navigation component
<NavigationMenuItem>
  <Link href="/admin/versions">
    <NavigationMenuLink>Versions</NavigationMenuLink>
  </Link>
</NavigationMenuItem>
```

## Related Documentation
- See `Docs/07-ADMIN-GUIDE.md` for admin features overview
- See shadcn/ui docs for component usage
