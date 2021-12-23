<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <el-form ref="queryParams" :model="queryParams" size="small" :inline="true">
      <el-form-item>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd"
          >新增</el-button
        >
        <!-- <el-button type="success" icon="el-icon-edit" :disabled="single" @click="handleUpdate">修改</el-button> -->
        <el-button
          type="danger"
          icon="el-icon-delete"
          :disabled="multiple"
          @click="handleDelete"
          >删除</el-button
        >
      </el-form-item>
      <el-form-item prop="case_name">
        <el-input
          v-model="queryParams.case_name"
          placeholder="用例名称"
          clearable
          style="width: 180px"
          @keyup.enter.native="showTestcase"
        />
        <el-select v-model="queryParams.project" placeholder="所属项目" style="width: 140px" >
           <el-option v-for="item in options" :key="item.prj_id" :label="item.prj_name" :value="item.prj_id"/>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="showTestcase"
          >搜索</el-button
        >
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 列表数据 -->
    <el-table v-loading="loading" :data="testcaseList" border @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column prop="case_name" label="用例名称" min-width="70">
        <template slot-scope="scope">
          {{ scope.row.fields.case_name|ellipsis }}
        </template>
      </el-table-column>
      <!-- <el-table-column prop="if_name" label="对应接口" min-width="80">
        <template slot-scope="scope"> {{ scope.row.fields.description|ellipsis }} </template>
      </el-table-column> -->
      <el-table-column prop="project" label="所属项目" min-width="60" >
        <template slot-scope="scope" >
          {{ get_map_prj(scope.row.fields.project) }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="用例描述" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.description|ellipsis }} </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="180" align="center">
        <template slot-scope="scope">
           <el-button
           type="success"
            size="mini"
            round
            plain
            @click.stop="handRun(scope.row)"
          >运行</el-button>
          <el-button
            type="primary"
            icon="el-icon-edit"
            size="mini"
            circle
            plain
            @click.stop="handleUpdate(scope.row.pk)"
          />
          <el-button
            type="danger"
            icon="el-icon-delete"
            size="mini"
            circle
            plain
            @click.stop="handleDelete(scope.row.pk)"
          />
        </template>
      </el-table-column>
    </el-table>
    <!-- 列表翻页 -->
    <div class="sc-pagination-container">
      <ul>
        <el-pagination
          background
          layout="total,prev, pager, next"
          v-show="pagination.total > 0"
          :total="pagination.total"
          :page-size="pagination.limit"
          @current-change="handleCurrentChange"
        >
        </el-pagination>
      </ul>
    </div>

    <!-- run表单弹窗 -->
    <el-dialog
      :title="rundialog.title"
      :visible.sync="rundialog.visible"
      width="550px"
    >
      <el-form ref="form" :model="test_dialog" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="20">
            <el-form-item label="选择运行环境" prop="if_name">
              <el-select v-model="test_dialog.env" placeholder="请选择">
                <el-option
                  v-for="item in test_dialog.env_list"
                  :key="item.env_id"
                  :label="item.env_name"
                  :value="item.env_id"
                >
                </el-option>
              </el-select>
            </el-form-item>
            <el-form-item label="接口返回值" >
              <el-input type="textarea" :rows="6" v-model="test_dialog.response"/>
            </el-form-item>
            <el-form-item label="测试结果">
              <el-input type="text" v-model="test_dialog.test_result"/>
            </el-form-item>
          </el-col>
        </el-row> 
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="rundialog.visible = false" >取 消</el-button>
        <el-button type="primary" @click="handleTest(test_dialog.case_id,test_dialog.env)" >调 试</el-button>
      </div>
    </el-dialog>
    <!-- 新增及修改弹框 -->
    <el-dialog
      :title="dialog.title"
      :visible.sync="dialog.visible"
      width="600px"
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <!-- 用例名称 -->
          <el-col :span="12">
            <el-form-item label="用例名称" prop="case_name">
              <el-input v-model="form.case_name" placeholder="请输入用例名称" />
            </el-form-item>
          </el-col>
        <!-- 所属项目 -->
          <el-col :span="12">
            <el-form-item label="所属项目" prop="project">
              <el-select v-model="form.project" placeholder="请选择" @change="getinterface_by_prj">
                <el-option
                  v-for="item in options"
                  :key="item.prj_id"
                  :label="item.prj_name"
                  :value="item.prj_id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
        <el-form-item label="用例描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            placeholder="用例描述"
          />
        </el-form-item>
        </el-row>
        <!-- 添加步骤 -->
        <el-row>
            <el-form-item label="添加步骤" prop="content">
              <el-select v-model="form.if_id" placeholder="请选择接口" >
                <el-option
                  v-for="item in interface_obj"
                  :key="item.if_id"
                  :label="item.if_name"
                  :value="item.if_id"
                >
                </el-option>
              </el-select>
              <el-button style="position: absolute; right: 190px" type="primary" @click="insertdata(form.if_id)">确定</el-button> 
            </el-form-item>
        </el-row> 
        <!-- 请求头、体、响应头、体 -->
        <!-- 请求header -->
        <el-row v-if="true" >
            <div v-for="(items,indexs) in form.content" :key="indexs">
            <div class="boders">
                 <el-row>
                   <el-col align="center">
                     <el-row>{{items.if_name}}</el-row>
                   </el-col>
                 </el-row> 
            </div>
            <el-row>
            <el-button type="primary" round size="small"  @click="addRow(indexs,flag_motai.request_header)">添加heard参数</el-button>
            <el-button type="primary" round size="small"  @click="addRow(indexs,flag_motai.request_body)">添加body参数</el-button>
            <el-button type="primary" round size="small"  @click="addRow(indexs,flag_motai.extract)">添加提取参数</el-button>
            <el-button type="primary" round size="small"  @click="addRow(indexs,flag_motai.validators)">添加检查点</el-button>
            <el-button type="primary" round size="small"  @click="deleteifobj(indexs)">删除本接口</el-button>
            </el-row>
          <el-form-item label="请求header">
            <el-table :data="items.header">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="items.header[scope.$index].var_name"/>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值"> 
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="items.header[scope.$index].var_remark"/>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" autosize icon="el-icon-delete" round @click="deleteRow(flag_motai.request_header,indexs,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item>
        <!-- 请求body -->
          <el-form-item  label="请求body" >
            <el-table :data="items.body">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="items.body[scope.$index].var_name"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize  v-model="items.body[scope.$index].var_remark"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" icon="el-icon-delete" round @click="deleteRow(flag_motai.request_body,indexs,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item> 
        <!-- 返回header -->
          <el-form-item  label="返回header" > 
            <el-table :data="items.response_header">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" disabled='disabled' autosize v-model="items.response_header[scope.$index].var_name"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" disabled='disabled' autosize  v-model="items.response_header[scope.$index].var_remark"></el-input>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item> 
        <!-- 返回body -->
        <el-form-item  label="返回body" >
            
            <el-table :data="items.response_body">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" disabled='disabled' autosize v-model="items.response_body[scope.$index].var_name"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" disabled="disabled" autosize  v-model="items.response_body[scope.$index].var_remark"></el-input>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item> 
          <!-- 提取参数 -->
          <el-form-item  label="提取参数" >
            
            <el-table :data="items.extract">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="items.extract[scope.$index].var_name"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" icon="el-icon-delete" round @click="deleteRow(flag_motai.extract,indexs,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item> 
          <!-- 检查点 -->
          <el-form-item  label="检查点" >
            
            <el-table :data="items.validators">
            <el-table-column prop="check" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="items.validators[scope.$index].check"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="expect" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize  v-model="items.validators[scope.$index].expect"></el-input>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" icon="el-icon-delete" round @click="deleteRow(flag_motai.validators,indexs,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item> 
            </div>
        </el-row>
        
        <!-- 以上为可控的弹框内容 -->
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleSubmit" >保 存</el-button>
        <el-button @click="dialog.visible = false" >取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>
<script>
import { getprj,get_project_interface_case_all} from "@/api/interface"
import {gettestcase,getinterfacecontent_by_prj_id,add,del,detail,update,case_run} from '@/api/testcase'
export default {
  // name: 'test1',
  data() {
    return {
      //默认非多选时【删除】按钮不可点
      multiple:true,
      //多选选中的列表
      testcase_ids:[],
      //列表数据列表
      testcaseList: [],
      //列表数据列表中的content
      testcaseListcontent:[],
      //新增表单中添加的各项标识
      flag_motai:{
        request_header:"1",
        request_body:"2",
        extract:"3",
        validators:"4"
      },
      loading: false,
      meg: "",
      queryParams: {
        case_name: undefined,
        project: undefined
      },
      //新增及修改弹框参数
      dialog: {
        title: undefined,
        visible: false,
        type: undefined, // type 操作类型：1-新增 2-修改
      },
      //运行弹框参数
      rundialog:{
          title:undefined,
          visible: false,
      },
      //调试弹框中的环境、运行结果、返回值
      test_dialog:{
          env_list:[],
          response:undefined,
          test_result:undefined,
          env:undefined,
          case_id:undefined
      },
      pagination: {
        page: 1,
        limit: 5,
        total: 0,
      },
      form: {
        testcase_id:undefined,
        case_name: undefined,
        description: undefined,
        project: undefined,
        content:[],
      },
      //存储首页项目下拉值
      options:[],
      interface_obj:[],
      rules: {
        case_name: [
          { required: true, message: "用例名称不能为空", trigger: "blur" },
        ],
        project: [
          { required: true, message: "请选择项目", trigger: "blur" },
        ],
        content: [
          { required: true, message: "请选择接口", trigger: "blur" },
        ],
      },
    };
  },
  mounted: function () {
    this.getprojectparm();
    this.showTestcase()
    

  },
  methods: {
     addRow(index,flag) {
       if(flag=='1'){
          this.form.content[index].header.push({});
       }else if(flag=='2'){
          this.form.content[index].body.push({});
       }else if(flag=='3'){
         this.form.content[index].extract.push({});
       }else{
         this.form.content[index].validators.push({});
       }
      
    },
    //弹框中insert 函数
    insertdata(interface_id){
      const datas={if_id:interface_id,prj_id:undefined}
      getinterfacecontent_by_prj_id(datas).then((response)=>{
          this.form.content.push(response)
      })
      console.log(this.form)
    },
    //接口对象项删除
    deleteRow(flag,index,parm_index) {
      if(flag=='1'){
          this.form.content[index].header.splice(parm_index, 1);
      }else if(flag=='2'){
          this.form.content[index].body.splice(parm_index, 1);
      }else if(flag=='3'){
          this.form.content[index].extract.splice(parm_index, 1);
      }else if(flag=='4'){
          this.form.content[index].validators.splice(parm_index, 1);
      }
    },
    //接口删除
    deleteifobj(index){
        this.form.content.splice(index,1)
    },
    //首页搜索中的项目下拉选项
    getprojectparm(){
        getprj().then((response)=>{
          this.options=response.data
        })
    },
    showTestcase() {
      this.queryParams.page = this.pagination.page;
      this.queryParams.limit = this.pagination.limit;
      gettestcase(this.queryParams).then((response) => {
        this.testcaseList = response.data.data;
        this.pagination.total = response.data.totalCount;
      });
    },
    handleAdd() {
      this.resetForm();
      this.dialog = {
        title: "新增用例",
        visible: true,
        type: "add",
      };
    },
    handRun(obj){
      this.rundialog = {
        title: "用例调试",
        visible: true
      } 
      const prj_id=obj.fields.project
      const flag="get_env_by_prj_id"
      this.test_dialog.case_id=obj.pk
      get_project_interface_case_all(prj_id,flag).then((response)=>{
          this.test_dialog.env_list=response.data
      })
      
    },
    //
    handleTest(case_id,env_id){
        const data={case_id:case_id,env_id:env_id}
        case_run(data).then((response)=>{
            this.test_dialog.response=JSON.stringify(response.data.step_list)
            this.test_dialog.test_result=response.data.result
        })
    },
    handleUpdate(row) {
      this.dialog = {
        title: "修改用例",
        visible: true,
        type: "edit",
      };
      const id = row;
      detail(id).then((response) => {
        this.form=response.data
        console.log(this.form)
        // this.form.contents.header=eval(response.data[0].fields.request_header_param)
      });
    },
    //列表多选操作
    handleSelectionChange(selection){
        this.testcase_ids=selection.map(item=>item.pk)
        this.multiple=selection.length === 0
    },
    closeDialog() {
      this.dialog = {
        title: undefined,
        visible: false,
        type: undefined,
      };
    },
    resetForm() {
      this.form = {
        testcase_id:undefined,
        case_name: undefined,
        description: undefined,
        project: undefined,
        content:[],
      };
      if (this.$refs["form"]) {
        this.$refs["form"].resetFields();
      }
    },
    handleSubmit: function () {
      this.$refs["form"].validate((valid) => {
        if (valid) {
          // this.form.authorizedGrantTypes = this.form.authorizedGrantTypes.join(',')
          if (this.dialog.type == "edit") {
            update(this.form.testcase_id, this.form).then(() => {
              this.$message.success("修改成功");
              this.closeDialog();
              this.showTestcase();
            });
          } else {
            add(this.form).then(() => {
              this.$message.success("新增成功");
              this.closeDialog();
              this.resetForm();
              this.showTestcase();
            });
          }
        }
      });
    },
    handleDelete(testcase_ids) {
      if(this.testcase_ids.length>0){
          testcase_ids=this.testcase_ids
      }
      this.$confirm("确认删除该接口?", "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          del(testcase_ids).then(() => {
            this.$message.success("删除成功");
            this.showTestcase();
          });
        })
        .catch(() => this.$message.info("已取消删除"));
    },
    handleReset() {
      this.pagination = {
        page: 1,
        limit: 5,
        total: 0,
      };
      this.queryParams = {
        case_name: undefined,
        project: undefined
      };
      this.showTestcase();
    },
    handleCurrentChange(val) {
      this.pagination.page = val;
      this.queryParams.page = this.pagination.page;
      this.queryParams.limit = this.pagination.limit;
      gettestcase(this.queryParams).then((response) => {
        this.testcaseList = response.data.data;
        this.pagination.total = response.data.totalCount;
      });
    },
    get_map_prj(project){
        let lable=""
        this.options.forEach(item=>{
          if(item.prj_id===project){
              lable=item.prj_name
          }
        })
        return lable
    },
    //通过下拉选择项目触发接口
    getinterface_by_prj(prj_id){
        const data={prj_id:prj_id,if_id:undefined}
        getinterfacecontent_by_prj_id(data).then((response)=>{
            this.interface_obj=undefined
            this.interface_obj=response.data
        })
    },
    // 文件上传前校验文件格式方法
    onbeforeupload(file){
        const isexcel=file.type==="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if(!isexcel){
          this.$message.error("上传的文件类型不行，只能上传Excel!");
        }
    },
    //文件上传成功后的回掉函数
    onuploadsuccess(res){
        if(res.code===0){
            this.$message.success(res.message)
        }else{
            this.$message.error(res.message)
        }
    },
  },
  //计算属性
  computed:{
     downloadtemplete(){
       return "http://127.0.0.1:9529/apitest/download_file"
     }
  },
  filters:{
//     get_map_prj(type){
        
//         const maps=new Map([
//         ['1','办事员'],
//         ['2','科员'],
//               ])
//         return maps.get(type)
//     }
  //指定字符串字段过长时超出部分现实省略号过滤器
  ellipsis(value){
    if(!value) return ''
    if(value.length>15){
        return value.slice(0,15) + '......'
    }
    return value
  }
  },
  components: {},
};
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1,
h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  /* display: inline-block; */
  margin: 0 5px;
}

a {
  color: #42b983;
}
.el-upload__tip {
    font-size: 12px;
    color: #606266;
    margin-top: -5px;
}
.boders{
  font-size: 18px;
  font-weight: 300;
  color: #020813fa;
  margin-top: 0%;
  margin-bottom: 5%;
}
</style>



