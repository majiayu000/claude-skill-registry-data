---
name: dev-asp-net
description: DevExpress 25.1.6.0을 활용한 ASP.NET 웹 페이지 개발 전문가 스킬. ASP.NET Web Forms, MVC 패턴, DevExpress Bootstrap 컨트롤, Bootstrap 반응형 디자인 작업 시 사용. (1) ASP.NET 웹 페이지 생성, (2) DevExpress Bootstrap 컨트롤(BootstrapGridView, BootstrapComboBox, BootstrapDateEdit, BootstrapButton, BootstrapSpinEdit 등) 구현, (3) XPO DataBinding 설정, (4) PopupEditForm 편집 패턴 구현, (5) Code-behind 작성 시 사용.
---

# DevAspNet Skill

DevExpress Bootstrap 25.1.6.0 기반 ASP.NET 웹 개발 가이드.

## 핵심 원칙

### 아키텍처 패턴
- **MVC 패턴**: Controller에서 비즈니스 로직, View에서 UI 분리
- **DataBinding**: List<ViewModel> 기반 바인딩, 세션 캐싱 활용
- **반응형 디자인**: Bootstrap 5.3 + DevExpress Bootstrap 컨트롤

### 코드 작성 규칙
1. **ASPX 주석**: `<%-- 주석 --%>` (HTML 주석 금지)
2. **한글 주석**: 복잡한 로직에 필수
3. **File Encoding**: 한글이 안깨지도록 UTF-8로 저장
4. **출력 형식**: 변경 파일 리스트와 소스만 제공
5. **문서**: 최소한의 요약 md만 생성

## DevExpress Bootstrap 컨트롤

### Register 지시문
```aspx
<%@ Register Assembly="DevExpress.Web.Bootstrap.v25.1, Version=25.1.6.0, Culture=neutral, PublicKeyToken=b88d1754d700e49a" 
    Namespace="DevExpress.Web.Bootstrap" TagPrefix="dx" %>
```

### BootstrapGridView 기본 구조
```aspx
<dx:BootstrapGridView ID="gridToDoList" runat="server"
    ClientInstanceName="gridToDoList"
    Width="100%"
    KeyFieldName="COMPANY_NO;CASE_NO;PROJECT_NO;ORDER_NO"
    AutoGenerateColumns="False"
    EnableCallBacks="true"
    OnPageIndexChanged="grid_PageIndexChanged"
    OnCustomCallback="grid_CustomCallback"
    OnRowUpdating="grid_RowUpdating"
    OnHtmlRowPrepared="grid_HtmlRowPrepared">

    <Settings
        ShowFilterRow="True"
        ShowFilterRowMenu="True"
        VerticalScrollBarMode="Visible"
        VerticalScrollableHeight="450"
        HorizontalScrollBarMode="Auto" />

    <SettingsBehavior
        AllowFocusedRow="True"
        AllowSelectByRowClick="True" />

    <SettingsDataSecurity
        AllowEdit="True"
        AllowInsert="False"
        AllowDelete="False" />

    <SettingsPager Mode="ShowPager" PageSize="50" Position="Bottom">
        <PageSizeItemSettings Visible="true" Items="50,100,200,500" />
    </SettingsPager>

    <Columns>
        <%-- 컬럼 정의 --%>
    </Columns>
</dx:BootstrapGridView>
```

### BootstrapGridView 컬럼 타입
```aspx
<%-- 텍스트 컬럼 --%>
<dx:BootstrapGridViewTextColumn FieldName="ORDER_NAME" Caption="지시명칭" Width="200px" ReadOnly="true" VisibleIndex="1">
    <CssClasses HeaderCell="header-basic text-center" />
</dx:BootstrapGridViewTextColumn>

<%-- 날짜 컬럼 --%>
<dx:BootstrapGridViewDateColumn FieldName="COMP_DATE" Caption="완료일" Width="120px" VisibleIndex="2">
    <PropertiesDateEdit DisplayFormatString="yyyy-MM-dd" AllowNull="true" />
    <CssClasses HeaderCell="header-editable text-center" />
</dx:BootstrapGridViewDateColumn>

<%-- 숫자(SpinEdit) 컬럼 --%>
<dx:BootstrapGridViewSpinEditColumn FieldName="PLAN_MHR" Caption="계획 M/H" Width="100px" VisibleIndex="3">
    <PropertiesSpinEdit DisplayFormatString="N1" MinValue="0" MaxValue="99999" AllowNull="true" />
    <CssClasses HeaderCell="header-editable text-center" />
</dx:BootstrapGridViewSpinEditColumn>

<%-- 명령 버튼 컬럼 --%>
<dx:BootstrapGridViewCommandColumn Width="60px" ShowEditButton="True" VisibleIndex="0" Caption=" ">
    <CssClasses HeaderCell="text-center" />
</dx:BootstrapGridViewCommandColumn>

<%-- 숨김 Key 컬럼 --%>
<dx:BootstrapGridViewTextColumn FieldName="COMPANY_NO" Visible="false" />
```

### PopupEditForm 설정
```aspx
<dx:BootstrapGridView ...>
    <%-- PopupEditForm 방식 설정 --%>
    <SettingsEditing Mode="PopupEditForm" />
    <SettingsPopup>
        <EditForm 
            HorizontalAlign="WindowCenter" 
            VerticalAlign="WindowCenter" 
            Modal="True" 
            PopupAnimationType="Auto" />
    </SettingsPopup>
    <SettingsText
        CommandEdit="수정"
        CommandUpdate="저장"
        CommandCancel="취소"
        PopupEditFormCaption="작업지시 수정" />

    <%-- EditForm 템플릿 --%>
    <Templates>
        <EditForm>
            <div style="padding: 20px; min-width: 350px;">
                <table class="table" style="margin-bottom: 15px;">
                    <tr>
                        <td style="width: 120px; font-weight: bold;">완료일</td>
                        <td>
                            <dx:BootstrapDateEdit ID="edtCompDate" runat="server"
                                Width="100%"
                                DisplayFormatString="yyyy-MM-dd"
                                EditFormat="Date"
                                AllowNull="true"
                                Value='<%# Bind("COMP_DATE") %>' />
                        </td>
                    </tr>
                    <tr>
                        <td style="font-weight: bold;">계획 M/H</td>
                        <td>
                            <dx:BootstrapSpinEdit ID="edtPlanMhr" runat="server"
                                Width="100%"
                                DisplayFormatString="N1"
                                MinValue="0" MaxValue="99999"
                                AllowNull="true"
                                Value='<%# Bind("PLAN_MHR") %>' />
                        </td>
                    </tr>
                </table>
                <div style="text-align: right; padding-top: 10px; border-top: 1px solid #ddd;">
                    <dx:BootstrapButton ID="btnUpdate" runat="server" Text="저장" AutoPostBack="false">
                        <SettingsBootstrap RenderOption="Primary" />
                        <ClientSideEvents Click="function(s, e) { gridToDoList.UpdateEdit(); }" />
                    </dx:BootstrapButton>
                    <dx:BootstrapButton ID="btnCancel" runat="server" Text="취소" AutoPostBack="false" CssClasses-Control="ml-2">
                        <SettingsBootstrap RenderOption="Secondary" />
                        <ClientSideEvents Click="function(s, e) { gridToDoList.CancelEdit(); }" />
                    </dx:BootstrapButton>
                </div>
            </div>
        </EditForm>
    </Templates>
</dx:BootstrapGridView>
```

### 클라이언트 메시지 콜백 패턴
```aspx
<ClientSideEvents EndCallback="function(s, e) {
    if (s.cpMessage) {
        alert(s.cpMessage);
        s.cpMessage = null;
    }
}" />
```

### BootstrapComboBox
```aspx
<dx:BootstrapComboBox ID="cmbCompany" runat="server" 
    Width="250px" 
    AutoPostBack="false" />

<%-- AutoPostBack 사용 시 --%>
<dx:BootstrapComboBox ID="cmbCompanyType" runat="server" 
    Width="150px" 
    OnSelectedIndexChanged="cmbCompanyType_SelectedIndexChanged" 
    AutoPostBack="true" />
```

### BootstrapDateEdit
```aspx
<dx:BootstrapDateEdit ID="dtBaseDate" runat="server" 
    Width="150px" 
    DisplayFormatString="yyyy-MM-dd" 
    EditFormat="Date" 
    AllowNull="false" />
```

### BootstrapButton
```aspx
<%-- Primary 버튼 (아이콘 포함) --%>
<dx:BootstrapButton ID="btnSearch" runat="server"
    Text="<i class='fas fa-search'></i> 조회"
    EncodeHtml="false"
    OnClick="btnSearch_Click">
    <SettingsBootstrap RenderOption="Primary" />
</dx:BootstrapButton>

<%-- 확인 다이얼로그 --%>
<dx:BootstrapButton ID="btnDelete" runat="server"
    Text="<i class='fas fa-times'></i> 삭제"
    EncodeHtml="false"
    OnClick="btnDelete_Click">
    <SettingsBootstrap RenderOption="Danger" />
    <ClientSideEvents Click="function(s, e) {
        e.processOnServer = confirm('선택한 데이터를 삭제하시겠습니까?');
    }" />
</dx:BootstrapButton>
```

## Code-behind 패턴

### 기본 구조
```csharp
using DevExpress.Web;
using DevExpress.Web.Bootstrap;
using DevExpress.Web.Data;

public partial class ToDoList : System.Web.UI.Page
{
    private ToDoListController _controller = new ToDoListController();
    private const string SESSION_KEY_DATA = "ToDoList_Data";

    // 세션 기반 그리드 데이터 관리
    private List<ToDoListViewModel> GridData
    {
        get { return Session[SESSION_KEY_DATA] as List<ToDoListViewModel>; }
        set { Session[SESSION_KEY_DATA] = value; }
    }

    protected void Page_Load(object sender, EventArgs e)
    {
        // 로그인 체크
        if (Session["UserID"] == null)
        {
            Response.Redirect("Login.aspx", false);
            Context.ApplicationInstance.CompleteRequest();
            return;
        }

        if (!IsPostBack && !IsCallback)
            InitializePage();
        else
            BindGridFromSession();
    }
}
```

### 복합 키 RowUpdating 처리 (중요!)
```csharp
protected void grid_RowUpdating(object sender, ASPxDataUpdatingEventArgs e)
{
    // List<T> 데이터소스는 기본 업데이트 미지원 → 항상 Cancel
    e.Cancel = true;

    try
    {
        // 복합키: e.Keys로 접근 (e.OldValues 아님!)
        string companyNo = e.Keys["COMPANY_NO"]?.ToString();
        string caseNo = e.Keys["CASE_NO"]?.ToString();
        string projectNo = e.Keys["PROJECT_NO"]?.ToString();
        string orderNo = e.Keys["ORDER_NO"]?.ToString();

        // 수정 필드: e.NewValues로 접근
        DateTime? compDate = e.NewValues["COMP_DATE"] as DateTime?;
        decimal? planMhr = e.NewValues["PLAN_MHR"] as decimal?;

        bool result = _controller.UpdateWorkOrder(
            caseNo, companyNo, projectNo, orderNo,
            compDate, planMhr, userId);

        if (result)
        {
            // 성공 시: 팝업 닫고 데이터 새로고침
            gridToDoList.CancelEdit();
            LoadData();
            ShowMessageCallback("데이터가 수정되었습니다.");
        }
    }
    catch (Exception ex)
    {
        ShowMessageCallback($"수정 오류: {ex.Message}");
    }
}
```

### 콜백 메시지 표시
```csharp
// 일반 메시지
private void ShowMessage(string message)
{
    string script = $"alert('{message.Replace("'", "\\'")}');";
    ScriptManager.RegisterStartupScript(this, GetType(), "alertScript", script, true);
}

// 콜백 모드 메시지 (JSProperties 사용)
private void ShowMessageCallback(string message)
{
    gridToDoList.JSProperties["cpMessage"] = message;
}
```

### 세션 바인딩
```csharp
private void BindGridFromSession()
{
    if (GridData != null)
    {
        gridToDoList.DataSource = GridData;
        gridToDoList.DataBind();
    }
}
```

### 행 삭제 (FocusedRow 사용)
```csharp
protected void btnDelete_Click(object sender, EventArgs e)
{
    if (gridToDoList.FocusedRowIndex < 0)
    {
        ShowMessage("삭제할 데이터를 선택하세요.");
        return;
    }

    // 복합키 가져오기
    object[] keyValues = (object[])gridToDoList.GetRowValues(
        gridToDoList.FocusedRowIndex,
        new string[] { "COMPANY_NO", "CASE_NO", "PROJECT_NO", "ORDER_NO" });

    string companyNo = keyValues[0]?.ToString();
    string caseNo = keyValues[1]?.ToString();
    // ...
}
```

## 주의사항

1. **ASPxGridView vs BootstrapGridView**: 이 프로젝트는 `BootstrapGridView` 사용
2. **PopupEditForm 성공 시**: `gridToDoList.CancelEdit()` 호출로 팝업 닫기
3. **복합 키**: `KeyFieldName="Key1;Key2;Key3"` 세미콜론 구분, `e.Keys`로 접근
4. **List<T> 데이터소스**: `e.Cancel = true` 필수 (기본 업데이트 미지원)
5. **콜백 메시지**: `JSProperties["cpMessage"]` + `EndCallback` 이벤트 조합