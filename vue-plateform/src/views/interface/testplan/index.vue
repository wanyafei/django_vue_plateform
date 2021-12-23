<template>
<div class="app-container">
  <!-- 搜索表单 -->
    <el-form
      ref="queryParams"
      :model="queryParams"
      size="small"
      :inline="true"
    >
      <el-form-item>
        <el-button type="primary" icon="el-icon-plus" @click="handleAdd">新增</el-button>
        <!-- <el-button type="success" icon="el-icon-edit" :disabled="single" @click="handleUpdate">修改</el-button>
        <el-button type="danger" icon="el-icon-delete" :disabled="multiple" @click="handleDelete">删除</el-button> -->
      </el-form-item>
      <el-form-item prop="plan_name">
        <el-input
          v-model="queryParams.plan_name"
          placeholder="计划名称"
          clearable
          style="width: 220px"
          @keyup.enter.native="showPlan"
        />
        <el-select v-model="queryParams.project" placeholder="所属项目" style="width: 140px" >
           <el-option v-for="item in options" :key="item.prj_id" :label="item.prj_name" :value="item.prj_id"/>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="el-icon-search" @click="showPlan">搜索</el-button>
        <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
      </el-form-item>
    </el-form>

    <!-- 列表数据 -->
    <el-table v-loading="loading"
              :data="planList"
              border             
    >
      <el-table-column prop="plant_name" label="计划名称" min-width="80">
      <template slot-scope="scope"> {{ scope.row.fields.plant_name }} </template>
      </el-table-column>
      <el-table-column prop="project" label="所属项目" min-width="80">
      <template slot-scope="scope"> 
        {{ get_map_prj(scope.row.fields.project) }}  
        </template>
      </el-table-column>
      <el-table-column prop="env" label="所属环境" min-width="80">
      <template slot-scope="scope"> 
        {{ get_map_env(scope.row.fields.env) }}
        </template>
      </el-table-column>
      <el-table-column prop="content" label="用例列表" min-width="100">
      <template slot-scope="scope">
        {{ scope.row.fold ? maxSlice(get_map_case(scope.row.fields.content)) : get_map_case(scope.row.fields.content) }}
        <div v-show="get_map_case(scope.row.fields.content).length > maxlength">
          <a  @click="scope.row.fold=false" v-show="scope.row.fold">展开</a>
          <a  @click="scope.row.fold=true" v-show="!scope.row.fold">收起</a>
        </div>
      </template>
      </el-table-column>
      <el-table-column prop="description" label="描述" min-width="80">
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
        <el-table-column fixed="right" label="报告" width="150">
        <template slot-scope="scope">
         <el-button
            type="success"
            size="mini"
            round
            plain
            @click.stop="handRun(scope.row.pk)"
          >执行</el-button>
          <el-button
            type="primary"
            size="mini"
            round
            plain
            @click.stop="queryReport(scope.row.pk)"
          >查看</el-button>
        </template>
      </el-table-column>
    </el-table>
    <div class="sc-pagination-container">
     <ul >
      <el-pagination
        background
        layout="total,prev, pager, next"
        v-show="pagination.total>0"
        :total="pagination.total"
        :page-size="pagination.limit"
        @current-change="handleCurrentChange">
      </el-pagination>
     </ul>
 </div>

    <!-- 表单弹窗 -->
    <el-dialog :title="dialog.title" :visible.sync="dialog.visible" width="600px">
      <el-form ref="form" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="14 ">
            <el-form-item label="计划名称" prop="plant_name">
              <el-input v-model="form.plant_name" placeholder="请输入测试计划名称"/>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row>
        <el-col :span="12">
            <el-form-item label="所属项目" prop="project">
              <el-select v-model="form.project" placeholder="请选择" @change="select_prj_option">
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
            <el-col :span="12">
            <el-form-item label="选择环境" prop="env">
              <el-select v-model="form.env" placeholder="请选择">
                <el-option
                  v-for="item in env_options"
                  :key="item.env_id"
                  :label="item.env_name"
                  :value="item.env_id"
                >
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          </el-row>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" placeholder="请输入测试计划描述"/>
        </el-form-item>
        <el-row>
            <el-form-item label="用例列表" prop="case_list">
              <el-button type="primary" @click="get_case(form.project)">获取用例</el-button>
              <el-checkbox-group v-model="def" format="changeStyle">
                <el-checkbox 
                    v-for="item in case_list_by_env"
                    :key="item.case_id"
                    :label="item.case_name"
                    @change="handleChange($event,item.case_id)">
                </el-checkbox>
              </el-checkbox-group>
            </el-form-item>
        </el-row>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
        <el-button @click="dialog.visible=false">取 消</el-button>
      </div>
    </el-dialog>
  </div>
</template>


<script>
import {getenv,getcase,getplan,add,detail,update,del,run_plan} from '@/api/testplan';
import {getprj,get_project_interface_case_all} from '@/api/interface';
export default {
  // name: 'test1',
  data () {
    return {
      maxlength:18,
      input: '',
      planList: [],
      loading: false,
      //项目option
      options: [],
      //env
      env:[],
      //用例
      case:[],
      //环境option
      env_options:[],
      //新增计划弹框中，存放用例列表数据
      case_list_by_env:[],
      //存储多选的选项
      store_case:[],
      //v_model取此值，没有默认0值使回显报错
      def:[0],
      queryParams: {
          plan_name: undefined,
          project:undefined
        },
      dialog: {
          title: undefined,
          visible: false,
          type: undefined  // type 操作类型：1-新增 2-修改
        },
      pagination: {
          page: 1,
          limit: 5,
          total: 0
        },
      form: {
          testplan_id:undefined,
          plant_name: undefined,
          env: undefined,
          project:undefined,
          case_list: [],
          description: undefined,
        },
      rules: {
          plant_name: [
            {required: true, message: '环境名称不能为空', trigger: 'blur'}
          ],
          case_list: [
            {required: true, message: '请选择用例', trigger: 'blur'}
          ],
          project:[
            {required:true,message:'请选择所属项目',trigger:'blur'}
          ],
          env: [
            {required: true, message: '请选择所属环境', trigger: 'blur'}
          ],
          description: [
            {required: false, message: '请输入接口描述', trigger: 'blur'}
          ]
        }
    }
  },
  mounted: function () {
    this.getprojectparm();
    this.getenvparm();
    this.getcaseparm();
    this.showPlan();
  },
  methods: {
    showPlan () {
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getplan(this.queryParams).then((response) => {
          this.planList = response.data.data
          this.pagination.total=response.data.totalCount
        })
    },
    handleAdd() {
        this.resetForm()
        this.dialog = {
          title: '添加计划',
          visible: true,
          type: 'add'
        }
      },
    handleUpdate(row) {
        this.dialog = {
          title: '修改计划  ',
          visible: true,
          type: 'edit'
        }
        const id = row
        detail(id).then(response => {
          this.form = response.data[0].fields
          this.form.testplan_id=response.data[0].pk
        })
      },
     closeDialog() {
        this.dialog = {
          title: undefined,
          visible: false,
          type: undefined
        }
      },
    maxSlice(info){
        return info.length>this.maxlength?info.slice(0,this.maxlength)+"...":info;
    },
    resetForm() {
        this.form = {
          testplan_id:undefined,
          plant_name: undefined,
          env: undefined,
          project:undefined,
          case_list: [],
          description: undefined,
        }
        if (this.$refs['form']) {
          this.$refs['form'].resetFields()
        }
      },
      //getproject事件
    getprojectparm(){
        getprj().then((response)=>{
          this.options=response.data
        })
    },
    //getenv事件
    getenvparm(){
        getenv().then((response)=>{
          this.env=response.data
        })
    },
    //getcase事件
    getcaseparm(){
      getcase().then((response)=>{
          this.case=response.data
      })
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
    get_map_env(env_id){
        let lable=""
        this.env.forEach(item=>{
          if(item.env_id===env_id){
              lable=item.env_name
          }
        })
        return lable
    },
    get_map_case(case_list){
      let lable=""
      eval(case_list).forEach(item=>{
        this.case.forEach(items=>{
            if(item===items.case_id){
                lable=lable+items.case_name+";"
            }
        })
      })
      return lable.substr(0,lable.length-1)
    },
    //通过下拉选择项目触发环境option
    select_prj_option(prj_id){
        const flag="get_env_by_prj_id"
        get_project_interface_case_all(prj_id,flag).then((response)=>{
          this.env_options=response.data
        })
    },
    //弹框中用例多选时触发的事件
    handleChange:function(e,case_id) {
      if(e){
        this.store_case.push(case_id);
      }else{
        this.delete(case_id);
      }
      this.form.case_list=this.store_case
    },
    handleSubmit: function () {
        this.$refs['form'].validate(valid => {
          if (valid) {
            if (this.dialog.type == 'edit') {
              update(this.form.testplan_id, this.form).then(() => {
                this.$message.success('修改成功')
                this.closeDialog()
                this.showPlan()
              })
            } else {
              add(this.form).then(() => {
                this.$message.success('添加成功')
                this.closeDialog()
                this.showPlan()
              })
            }
          }
        })
      },
    //执行
    handRun(plan_id){
      alert("开始运行,点击确定按钮后查看结果....")
      run_plan(plan_id).then((response)=>{
        alert(response.message)
      })
    },
    //查看报告
    queryReport(plan_id){
      //点击跳转至上次浏览页面
      // this.$router.go(-1)
      //指定跳转地址  
      const flag="plan"
      this.$router.push({path:'/get_report',query:{flag:flag,id:plan_id}})

    },
    //弹框中获取用例
    get_case(prj_id){
        const type="get_tc_by_prj_id"
        get_project_interface_case_all(prj_id,type).then((response)=>{
            this.case_list_by_env=response.data
        })
    },
    handleDelete(plan_id) {
        this.$confirm('确认删除该项目?', '警告', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          del(plan_id).then(() => {
            this.$message.success('删除成功')
            this.showPlan()
          })
        }).catch(() =>
          this.$message.info('已取消删除')
        )
      },
    handleReset() {
        this.pagination = {
          page: 1,
          limit: 5,
          total: 0
        }
        this.queryParams = {
          plan_name: undefined,
          project:undefined
        }
        this.showPlan()
      },
      handleCurrentChange(val) {
        this.pagination.page=val
        this.queryParams.page=this.pagination.page
        this.queryParams.limit=this.pagination.limit
        getplan(this.queryParams).then((response) => {
          this.planList = response.data.data
          this.pagination.total=response.data.totalCount
        })
      }
  },
    filters:{
  },
  components:{
    
  }

}
</script>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1, h2 {
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

</style>



