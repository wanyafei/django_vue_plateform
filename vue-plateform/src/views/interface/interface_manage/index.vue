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
      <el-form-item prop="if_name">
        <el-input
          v-model="queryParams.if_name"
          placeholder="接口名称"
          clearable
          style="width: 180px"
          @keyup.enter.native="showInterface"
        />
        <el-select v-model="queryParams.project" placeholder="所属项目" style="width: 140px" >
           <el-option v-for="item in options" :key="item.prj_id" :label="item.prj_name" :value="item.prj_id"/>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="showInterface"
          >搜索</el-button
        >
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </el-form-item>
      <el-form-item>
        <el-upload
          style="position: absolute; right: -250px"
          class="upload-demo"
          :before-upload="onbeforeupload"
          :on-success="onuploadsuccess"
          action="http://127.0.0.1:9529/apitest/upload_interface_templete"
        >
          <el-button size="small" type="primary"
            >上传<i class="el-icon-upload el-icon--right"></i
          ></el-button>
          <div 
          slot="tip" style="color:red" class="el-upload__tip">*只能上传excel文件

          </div>
        </el-upload>
        <el-link
          type="primary"
          :href="downloadtemplete"
          underline="false"
          style="position: absolute; right: -340px"
          icon="el-icon-download"
          >下载模版</el-link>
      </el-form-item>
    </el-form>

    <!-- 列表数据 -->
    <el-table v-loading="loading" :data="interfaceList" border @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column prop="if_name" label="接口名称" min-width="80">
        <template slot-scope="scope">
          {{ scope.row.fields.if_name }}
        </template>
      </el-table-column>
      <el-table-column prop="if_url" label="API地址" min-width="80">
        <template slot-scope="scope"> {{ scope.row.fields.if_url }} </template>
      </el-table-column>
      <el-table-column prop="method" label="请求方法" min-width="40">
        <template slot-scope="scope"> {{ scope.row.fields.method }} </template>
      </el-table-column>
      <el-table-column prop="project" label="所属项目" min-width="80" >
        <template slot-scope="scope" >
          {{ get_map_prj(scope.row.fields.project) }}
        </template>
      </el-table-column>
      <el-table-column prop="description" label="接口描述" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.description }} </template>
      </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
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

    <!-- 表单弹窗 -->
    <el-dialog
      :title="dialog.title"
      :visible.sync="dialog.visible"
      width="600px"
    >
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <!-- 接口名称 -->
          <el-col :span="18">
            <el-form-item label="接口名称" prop="if_name">
              <el-input v-model="form.if_name" placeholder="请输入接口名称" />
            </el-form-item>
          </el-col>
          <!-- API地址 -->
          <el-col :span="18">
            <el-form-item label="API地址" prop="if_url">
              <el-input v-model="form.if_url" placeholder="请输入api地址" />
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 所属项目 -->
        <el-row>
          <el-col :span="9">
            <el-form-item label="所属项目" prop="project">
              <el-select v-model="form.project" placeholder="请选择">
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
          <el-col :span="9">
            <el-form-item label="传输方式" prop="data_type">
              <el-select v-model="form.data_type" placeholder="请选择">
                <el-option
                  v-for="item in methods"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 请求方式 -->
        <el-row>
          <el-col :span="18">
            <el-form-item label="请求方式" prop="method">
              <el-radio-group v-model="form.method">
                <el-radio label="get">get</el-radio>
                <el-radio label="post">post</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 接口描述 -->
        <el-row>
        <el-form-item label="接口描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            placeholder="接口描述"
          />
        </el-form-item>
        </el-row>
        <!-- 请求header -->
        <el-row>
          <el-form-item label="请求header" prop="request_header">
            <el-button
              type="primary"
              round
              size="small"
              icon="el-icon-circle-plus-outline"
              @click="addRow(flag_motai.request_header)"
              >新增</el-button
            >
            <el-table :data="form.request_header">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="form.request_header[scope.$index].var_name"/>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize  v-model="form.request_header[scope.$index].var_remark"/>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" icon="el-icon-delete" round @click="deleteRow(flag_motai.request_header,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item>
        </el-row>
        <!-- 请求body -->
        <el-row>
          <el-form-item  label="请求body" prop="request_body">
            <el-button
              type="primary"
              round
              size="small"
              icon="el-icon-circle-plus-outline"
              @click="addRow(flag_motai.request_body)"
              >新增</el-button
            >
            <el-table :data="form.request_body">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="form.request_body[scope.$index].var_name"/>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize  v-model="form.request_body[scope.$index].var_remark"/>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" icon="el-icon-delete" round @click="deleteRow(flag_motai.request_body,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item>
        </el-row>
        <!-- 返回header -->
        <el-row>
          <el-form-item  label="返回header" prop="response_header">
            <el-button
              type="primary"
              round
              size="small"
              icon="el-icon-circle-plus-outline"
              @click="addRow(flag_motai.response_header)"
              >新增</el-button
            >
            <el-table :data="form.response_header">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="form.response_header[scope.$index].var_name"/>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize  v-model="form.response_header[scope.$index].var_remark"/>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" icon="el-icon-delete" round @click="deleteRow(flag_motai.response_header,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item>
        </el-row>
        <!-- 返回body -->
        <el-row>
          <el-form-item  label="返回body" prop="response_body">
            <el-button
              type="primary"
              round
              size="small"
              icon="el-icon-circle-plus-outline"
              @click="addRow(flag_motai.response_body)"
              >新增</el-button
            >
            <el-table :data="form.response_body">
            <el-table-column prop="var_name" label="参数名">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize v-model="form.response_body[scope.$index].var_name"/>
              </template>
            </el-table-column>
            <el-table-column prop="var_remark" label="值">
              <template slot-scope="scope">
                <el-input type="textarea" size="mini" autosize  v-model="form.response_body[scope.$index].var_remark"/>
              </template>
            </el-table-column>
            <el-table-column prop="" label="">
              <template slot-scope="scope">
                <el-button type="danger" size="small" icon="el-icon-delete" round @click="deleteRow(flag_motai.response_body,scope.$index)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          </el-form-item>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
        <el-button @click="dialog.visible = false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import { getinterface, getprj,detail, update, add, del,download_file,uploadapi } from "@/api/interface";
export default {
  // name: 'test1',
  data() {
    return {
      //默认非多选时【删除】按钮不可点
      multiple:true,
      //多选选中的列表
      if_ids:[],
      //列表数据列表
      interfaceList: [],
      flag_motai:{
        request_header:"1",
        request_body:"2",
        response_header:"3",
        response_body:"4"
      },
      loading: false,
      meg: "",
      queryParams: {
        if_name: undefined,
        project: undefined
      },
      dialog: {
        title: undefined,
        visible: false,
        type: undefined, // type 操作类型：1-新增 2-修改
      },
      pagination: {
        page: 1,
        limit: 5,
        total: 0,
      },
      form: {
        interface_id:undefined,
        if_name: undefined,
        if_url:undefined,
        description: undefined,
        project: undefined,
        method: undefined,
        data_type:undefined,
        request_header:[],
        request_body:[],
        response_header:[],
        response_body:[],
      },
      options: [],
      methods: [
        { value: "json", label: "json" },
        { value: "data", label: "data" },
      ],
      rules: {
        if_name: [
          { required: true, message: "接口名称不能为空", trigger: "blur" },
        ],
        if_url: [
          { required: true, message: "api地址不能为空", trigger: "blur" },
        ],
        project: [
          { required: true, message: "请选择项目", trigger: "blur" },
        ],
        method: [
          { required: true, message: "请选择请求方法", trigger: "blur" },
        ],
        data_type: [
          { required: true, message: "请选择传输类型", trigger: "blur" },
        ],
        request_header: [
          { required: true, message: "请添加请求头", trigger: "blur" },
        ],
        request_body: [
          { required: true, message: "请添加请求体", trigger: "blur" },
        ],
        response_header: [
          { required: false, message: "请添加响应头", trigger: "blur" }, 
        ],
        response_body: [
          { required: true, message: "请添加响应体", trigger: "blur" },
        ],
      },
    };
  },
  mounted: function () {
    this.getprojectparm();
    this.showInterface()
    

  },
  methods: {
     addRow(flag) {
       if(flag=='1'){
          this.form.request_header.push({});
       }else if(flag=='2'){
          this.form.request_body.push({});
       }else if(flag=='3'){
         this.form.response_header.push({});
       }else{
         this.form.response_body.push({});
       }
      
    },
    deleteRow(flag,index) {
      if(flag=='1'){
          this.form.request_header.splice(index, 1);
      }else if(flag=='2'){
          this.form.request_body.splice(index, 1);
      }else if(flag=='3'){
          this.form.response_header.splice(index, 1);
      }else{
          this.form.response_body.splice(index, 1);
      }
      
    },
    getprojectparm(){
        getprj().then((response)=>{
          this.options=response.data
        })
    },
    showInterface() {
      this.queryParams.page = this.pagination.page;
      this.queryParams.limit = this.pagination.limit;
      getinterface(this.queryParams).then((response) => {
        this.interfaceList = response.data.data;
        this.pagination.total = response.data.totalCount;
      });
    },
    handleAdd() {
      this.resetForm();
      this.dialog = {
        title: "新增接口",
        visible: true,
        type: "add",
      };
    },
    handleUpdate(row) {
      // this.resetForm()
      this.dialog = {
        title: "修改接口",
        visible: true,
        type: "edit",
      };
      const id = row;
      detail(id).then((response) => {
        this.form.if_name = response.data[0].fields.if_name;
        this.form.if_url = response.data[0].fields.if_url;
        this.form.method = response.data[0].fields.method;
        this.form.data_type = response.data[0].fields.data_type;
        this.form.project = response.data[0].fields.project;
        this.form.description = response.data[0].fields.description;
        this.form.interface_id = response.data[0].pk;
        this.form.method = response.data[0].fields.method;
        this.form.request_header=eval(response.data[0].fields.request_header_param);
        this.form.request_body=eval(response.data[0].fields.request_body_param);
        this.form.response_header=eval(response.data[0].fields.response_header_param);
        this.form.response_body=eval(response.data[0].fields.response_body_param);
        console.log(this.form);
      });
    },
    //列表多选操作
    handleSelectionChange(selection){
        this.if_ids=selection.map(item=>item.pk)
        this.multiple=selection.length === 0
    },
    closeDialog() {
      this.dialog = {
        title: undefined,
        visible: false,
        type: undefined,
      };
    },
    //下载接口模版方法
    download_templatefile(){
      download_file().then(()=>{
        this.$message.success("下载成功");
      })
    },
    resetForm() {
      this.form = {
        interface_id:undefined,
        if_name: undefined,
        if_url:undefined,
        description: undefined,
        project: undefined,
        method: undefined,
        data_type:undefined,
        request_header:[],
        request_body:[],
        response_header:[],
        response_body:[],
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
            update(this.form.interface_id, this.form).then(() => {
              this.$message.success("修改成功");
              this.closeDialog();
              this.showInterface();
            });
          } else {
            add(this.form).then(() => {
              this.$message.success("新增成功");
              this.closeDialog();
              this.resetForm();
              this.showInterface();
            });
          }
        }
      });
    },
    handleDelete(interface_ids) {
      if(this.if_ids.length>0){
          interface_ids=this.if_ids
      }
      this.$confirm("确认删除该接口?", "警告", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          del(interface_ids).then(() => {
            this.$message.success("删除成功");
            this.showInterface();
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
        if_name: undefined,
        project: undefined
      };
      this.showInterface();
    },
    handleCurrentChange(val) {
      this.pagination.page = val;
      this.queryParams.page = this.pagination.page;
      this.queryParams.limit = this.pagination.limit;
      getinterface(this.queryParams).then((response) => {
        this.interfaceList = response.data.data;
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
            this.showInterface()
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
</style>



